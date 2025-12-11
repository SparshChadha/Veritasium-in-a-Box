#!/usr/bin/env python3
"""
Standalone Multi-Agent Research Script (Enhanced)
Executes the same logic as kestra/multi-agent-research.yaml
without needing a Kestra server.

AGENTS:
- Historian: Wikipedia + Wikidata (Facts)
- Skeptic: Stack Exchange + NewsAPI (Debates/Myths)
- Professor: Semantic Scholar (Academic Papers)
"""

import json
import requests
import urllib.parse
import os  # <--- ADDED THIS
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# ==========================================
# AGENT 1: THE HISTORIAN (Context)
# ==========================================
def agent_historian(topic):
    """Historian: Wikipedia + Wikidata for structured facts"""
    print(f"🏛️  Agent Historian: Researching '{topic}'...")
    try:
        # 1. Wikipedia Summary
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(topic)}"
        headers = {'User-Agent': 'VeritasiumHackathonBot/1.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            wiki_result = {
                "title": data.get("title", ""),
                "extract": data.get("extract", ""),
                "url": data.get("content_urls", {}).get("desktop", {}).get("page", "")
            }
        else:
            wiki_result = {"error": "Wikipedia page not found"}

        # 2. Wikidata Facts (SPARQL)
        sparql_query = f"""
        SELECT ?item ?itemLabel ?description WHERE {{
          ?item rdfs:label "{topic}"@en .
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}
        }} LIMIT 1
        """
        sparql_url = "https://query.wikidata.org/sparql"
        sparql_params = {"query": sparql_query, "format": "json"}
        
        try:
            sparql_response = requests.get(sparql_url, params=sparql_params, timeout=5)
            wikidata = sparql_response.json().get("results", {}).get("bindings", [])
            facts = [{"label": i["itemLabel"]["value"], "desc": i.get("description", {}).get("value", "")} for i in wikidata]
        except:
            facts = []

        result = {
            "agent": "Historian",
            "topic": topic,
            "extract": wiki_result.get("extract", ""),
            "wiki_data": wiki_result,
            "wikidata_facts": facts,
            "status": "success"
        }
        print(f"   ✅ Historian: Found '{wiki_result.get('title', 'Unknown')}'")

    except Exception as e:
        result = {"agent": "Historian", "topic": topic, "error": str(e), "status": "failed"}
        print(f"   ❌ Historian: Failed - {str(e)}")
    return result

# ==========================================
# AGENT 2: THE SKEPTIC (Misconceptions)
# ==========================================
def agent_skeptic(topic):
    """Skeptic: Stack Exchange (High Quality) + NewsAPI"""
    print(f"🤔 Agent Skeptic: Searching debates on '{topic}'...")
    try:
        all_posts = []
        
        # 1. Stack Exchange (Physics, Skeptics, Science, Astronomy)
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
            except:
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
            except:
                pass

        result = {
            "agent": "Skeptic",
            "topic": topic,
            "posts": all_posts,
            "total_found": len(all_posts),
            "status": "success" if all_posts else "failed"
        }
        print(f"   ✅ Skeptic: Found {len(all_posts)} high-quality discussions")

    except Exception as e:
        result = {"agent": "Skeptic", "topic": topic, "error": str(e), "status": "failed"}
        print(f"   ❌ Skeptic: Failed - {str(e)}")
    return result

# ==========================================
# AGENT 3: THE PROFESSOR (Deep Dive)
# ==========================================
def agent_professor(topic):
    """Professor: Semantic Scholar (Better than ArXiv for general topics)"""
    print(f"🎓 Agent Professor: Searching Academic Papers on '{topic}'...")
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
        
        papers.sort(key=lambda x: x['citations'], reverse=True)

        result = {
            "agent": "Professor",
            "topic": topic,
            "papers": papers[:3],
            "total_found": len(papers),
            "status": "success"
        }
        print(f"   ✅ Professor: Found {len(papers)} papers via Semantic Scholar")

    except Exception as e:
        result = {"agent": "Professor", "topic": topic, "error": str(e), "status": "failed"}
        print(f"   ❌ Professor: Failed - {str(e)}")
    return result

# ==========================================
# ORCHESTRATOR
# ==========================================
def run_parallel_research(topic):
    """Execute all three agents in parallel"""
    print("=" * 70)
    print("🔬 TRIANGLE OF TRUTH - MULTI-AGENT RESEARCH (ENHANCED)")
    print("=" * 70)
    print(f"📋 Topic: {topic}")
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_historian = executor.submit(agent_historian, topic)
        future_skeptic = executor.submit(agent_skeptic, topic)
        future_professor = executor.submit(agent_professor, topic)
        
        historian_data = future_historian.result()
        skeptic_data = future_skeptic.result()
        professor_data = future_professor.result()
    
    return {
        "topic": topic,
        "timestamp": datetime.now().isoformat(),
        "agents": {
            "historian": historian_data,
            "skeptic": skeptic_data,
            "professor": professor_data
        },
        "summary": {
            "historian_status": historian_data.get("status"),
            "skeptic_status": skeptic_data.get("status"),
            "professor_status": professor_data.get("status")
        }
    }

def main():
    import sys
    # 1. Get Topic
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Enter research topic: ")
        
    # 2. Run Research
    results = run_parallel_research(topic)
    
    # 3. Save Output
    # FIXED: Removed 'ai-engine/' prefix since you are running INSIDE that folder
    output_file = "test_kestra_output.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
    print(f"\n✨ Research Complete! Saved to {output_file}")

if __name__ == "__main__":
    main()