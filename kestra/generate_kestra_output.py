#!/usr/bin/env python3
"""
Local development script to replicate the multi-agent-research Kestra flow functionality.

This script performs the same research as the Kestra workflow but runs locally for development/testing.

Requirements: pip install -r requirements.txt

Usage: python3 generate_kestra_output.py "The science of why time moves forward"

Output: ../research_outputs/kestra_output.json
"""

import json
import urllib.parse
import os
import sys
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

# Check for required packages
missing_packages = []

try:
    import requests
except ImportError:
    missing_packages.append("requests")

try:
    from slugify import slugify
except ImportError:
    missing_packages.append("python-slugify")

if missing_packages:
    print("❌ Missing required packages:", ", ".join(missing_packages))
    print("Please install them with:")
    print("   pip install -r requirements.txt")
    print("   or")
    print("   python3 -m pip install --user -r requirements.txt")
    print("   or manually:")
    for pkg in missing_packages:
        print(f"   pip install {pkg}")
    sys.exit(1)


def run_historian_research(topic):
    """Agent A: The Historian - Wikipedia + Wikidata"""
    print(f"🏛️ Historian researching: {topic}")
    try:
        # 1. Wikipedia Summary
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(topic)}"
        headers = {'User-Agent': 'VeritasiumHackathonBot/1.0'}
        response = requests.get(url, headers=headers, timeout=10)

        wiki_result = {}
        if response.status_code == 200:
            data = response.json()
            wiki_result = {
                "title": data.get("title", ""),
                "extract": data.get("extract", ""),
                "url": data.get("content_urls", {}).get("desktop", {}).get("page", "")
            }
        else:
            wiki_result = {"error": "Wikipedia page not found"}

        # 2. Wikidata Facts (SPARQL) - FIXED: Safe string building
        label_part = topic + '"@en'  # Build label safely
        sparql_query = """
        SELECT ?item ?itemLabel ?description WHERE {
          ?item rdfs:label "%s" .
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
        } LIMIT 1
        """ % label_part  # % formatting avoids {} conflicts

        sparql_url = "https://query.wikidata.org/sparql"
        sparql_params = {"query": sparql_query, "format": "json"}

        facts = []
        try:
            sparql_response = requests.get(sparql_url, params=sparql_params, timeout=5)
            if sparql_response.status_code == 200:
                wikidata = sparql_response.json().get("results", {}).get("bindings", [])
                facts = [{"label": i["itemLabel"]["value"], "desc": i.get("description", {}).get("value", "")} for i in wikidata]
        except Exception as e:
            print(f"Wikidata error: {e}")

        result = {
            "agent": "Historian",
            "topic": topic,
            "extract": wiki_result.get("extract", ""),
            "wiki_data": wiki_result,
            "wikidata_facts": facts,
            "status": "success"
        }
    except Exception as e:
        result = {
            "agent": "Historian",
            "topic": topic,
            "error": str(e),
            "status": "failed"
        }
    return result


def run_skeptic_research(topic):
    """Agent B: The Skeptic - Stack Exchange + NewsAPI"""
    print(f"🤔 Skeptic researching: {topic}")

    try:
        all_posts = []

        # 1. Stack Exchange
        stack_sites = ["physics", "skeptics", "science", "astronomy"]
        for site in stack_sites:
            try:
                url = "https://api.stackexchange.com/2.3/search/advanced"
                params = {
                    "site": site,
                    "q": topic,
                    "sort": "votes",
                    "pagesize": 2,
                    "order": "desc",
                    "filter": "!nNPvSNPH.z"
                }
                response = requests.get(url, params=params, timeout=5)
                if response.status_code == 200:
                    items = response.json().get("items", [])
                    for item in items:
                        all_posts.append({
                            "source": f"StackExchange ({site})",
                            "title": item.get("title", ""),
                            "snippet": item.get("body_markdown", "")[:200] + "...",
                            "score": item.get("score", 0),
                            "url": item.get("link", "")
                        })
            except Exception as e:
                print(f"StackExchange error ({site}): {e}")
                continue

        # 2. NewsAPI (Optional)
        news_key = os.environ.get("NEWS_API_KEY")
        if news_key:
            try:
                news_url = "https://newsapi.org/v2/everything"
                news_params = {
                    "apiKey": news_key,
                    "q": f"{topic} AND (myth OR misconception OR study)",
                    "sortBy": "relevancy",
                    "pageSize": 2,
                    "language": "en"
                }
                resp = requests.get(news_url, params=news_params, timeout=5)
                if resp.status_code == 200:
                    articles = resp.json().get("articles", [])
                    for art in articles:
                        all_posts.append({
                            "source": "NewsAPI",
                            "title": art.get("title", ""),
                            "snippet": art.get("description", ""),
                            "url": art.get("url", "")
                        })
            except Exception as e:
                print(f"NewsAPI error: {e}")

        result = {
            "agent": "Skeptic",
            "topic": topic,
            "posts": all_posts,
            "total_found": len(all_posts),
            "status": "success"
        }

    except Exception as e:
        result = {
            "agent": "Skeptic",
            "topic": topic,
            "error": str(e),
            "status": "failed"
        }

    return result


def run_professor_research(topic):
    """Agent C: The Professor - Semantic Scholar"""
    print(f"🎓 Professor researching: {topic}")

    try:
        # Semantic Scholar Graph API
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": topic,
            "limit": 5,
            "fields": "title,authors,abstract,year,citationCount,openAccessPdf"
        }
        headers = {"User-Agent": "VeritasiumHackathonBot/1.0"}

        response = requests.get(url, params=params, headers=headers, timeout=10)

        papers = []
        if response.status_code == 200:
            data = response.json().get("data", [])
            for p in data:
                if p.get("abstract"):
                    papers.append({
                        "title": p.get("title"),
                        "authors": [a["name"] for a in p.get("authors", [])[:2]],
                        "abstract": p.get("abstract")[:300] + "...",
                        "year": p.get("year"),
                        "citations": p.get("citationCount", 0),
                        "pdf_url": p.get("openAccessPdf", {}).get("url") if p.get("openAccessPdf") else None
                    })

        # Sort by citations
        papers.sort(key=lambda x: x.get('citations', 0), reverse=True)

        result = {
            "agent": "Professor",
            "topic": topic,
            "papers": papers[:3],
            "total_found": len(papers),
            "status": "success"
        }

    except Exception as e:
        result = {
            "agent": "Professor",
            "topic": topic,
            "error": str(e),
            "status": "failed"
        }

    return result


def main():
    parser = argparse.ArgumentParser(description="Generate multi-agent research output")
    parser.add_argument("topic", help="Research topic")
    parser.add_argument("--output-dir", default="../research_outputs", help="Output directory")
    parser.add_argument("--output", default="kestra_output.json", help="Output filename")

    args = parser.parse_args()
    topic = args.topic
    output_dir = args.output_dir

    print(f"🚀 Starting multi-agent research for: {topic}")
    start_time = time.time()

    # Run all three research agents in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(run_historian_research, topic): "historian",
            executor.submit(run_skeptic_research, topic): "skeptic",
            executor.submit(run_professor_research, topic): "professor"
        }

        results = {}
        for future in as_completed(futures):
            agent_name = futures[future]
            try:
                results[agent_name] = future.result()
            except Exception as e:
                print(f"Error in {agent_name}: {e}")
                results[agent_name] = {
                    "agent": agent_name.capitalize(),
                    "topic": topic,
                    "error": str(e),
                    "status": "failed"
                }

    # Extract agent data
    historian_data = results.get("historian")
    skeptic_data = results.get("skeptic")
    professor_data = results.get("professor")

    # Create combined research output
    combined_research = {
        "topic": topic,
        "timestamp": datetime.now().isoformat(),
        "agents": {
            "historian": historian_data,
            "skeptic": skeptic_data,
            "professor": professor_data
        },
        "summary": {
            "historian_status": historian_data.get("status", "unknown"),
            "skeptic_status": skeptic_data.get("status", "unknown"),
            "professor_status": professor_data.get("status", "unknown")
        }
    }

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Use configurable filename
    output_file = os.path.join(output_dir, args.output)

    # Write the combined research output
    try:
        with open(output_file, "w", encoding='utf-8') as f:
            json.dump(combined_research, f, indent=2, ensure_ascii=False)
        print(f"✅ SUCCESS: Saved research output to {output_file}")
    except Exception as e:
        print(f"❌ ERROR saving file: {e}")
        return 1

    # Print summary
    duration = time.time() - start_time
    print("\n" + "="*80)
    print("TRIANGLE OF TRUTH - COMBINED RESEARCH OUTPUT")
    print("="*80)
    print(f"Topic: {topic}")
    print(f"Duration: {duration:.1f}s")
    print(f"Output: {output_file}")
    print(f"Historian: {historian_data.get('status', 'unknown')}")
    print(f"Skeptic: {skeptic_data.get('status', 'unknown')}")
    print(f"Professor: {professor_data.get('status', 'unknown')}")
    print("="*80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
