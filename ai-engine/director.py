#!/usr/bin/env python3
"""
Director Agent - Merges Kestra research data with fine-tuned script output
Uses Together API to create a cohesive 5-minute Veritasium-style script
"""

import json
import os
from together import Together

# Configuration
KESTRA_OUTPUT = "ai-engine/test_kestra_output.json"
FINETUNED_SCRIPT = "ai-engine/finetuned_script.txt"
OUTPUT_SCRIPT = "ai-engine/final_5min_script.md"

def load_kestra_data(filepath):
    """Load and parse Kestra research data"""
    print(f"📊 Loading Kestra research data from {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Loaded {len(str(data))} characters of research data")
        return data
    except FileNotFoundError:
        print(f"❌ Error: {filepath} not found")
        print("   Please ensure the Kestra workflow has generated the research data.")
        raise
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {filepath}: {e}")
        raise

def load_finetuned_script(filepath):
    """Load fine-tuned model script output"""
    print(f"📝 Loading fine-tuned script from {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            script = f.read()
        print(f"✅ Loaded {len(script)} characters of script content")
        return script
    except FileNotFoundError:
        print(f"❌ Error: {filepath} not found")
        print("   Please run the fine-tuned model inference first.")
        raise

def merge_with_director_agent(kestra_data, finetuned_script):
    """
    Use Together API (Director Agent) to merge research and script
    Creates a cohesive 5-minute Veritasium-style video script
    """
    print("\n🎬 Activating Director Agent (Together API)...")
    
    # Get API key from environment
    api_key = os.environ.get("TOGETHER_API_KEY")
    if not api_key:
        raise ValueError(
            "❌ TOGETHER_API_KEY environment variable not set!\n"
            "   Please set it: export TOGETHER_API_KEY='your-api-key'"
        )
    
    client = Together(api_key=api_key)
    
    # Format the research data for the prompt
    kestra_summary = json.dumps(kestra_data, indent=2)
    
    # Create the director prompt
    director_prompt = f"""You are a Director Agent for creating Veritasium-style educational video scripts.

Your task: Merge research data from a multi-agent system (Kestra) with a draft script from a fine-tuned Llama model to create a polished, engaging 5-minute video script.

**RESEARCH DATA (from Kestra Multi-Agent System):**
```json
{kestra_summary}
```

**DRAFT SCRIPT (from Fine-Tuned Veritasium Model):**
{finetuned_script}

**YOUR MISSION:**
Create a final 5-minute Veritasium-style video script that:
1. **Integrates key facts** from the research data into the narrative
2. **Maintains the style** and flow from the fine-tuned script
3. **Adds scientific accuracy** using the research citations
4. **Structures for engagement**: Hook → Explanation → Twist/Revelation → Conclusion
5. **Targets 5 minutes** of speaking time (~750 words)

**OUTPUT FORMAT (Markdown):**
# [Compelling Title]

## Hook (0:00-0:30)
[Opening that grabs attention]

## Main Content (0:30-4:00)
[Core explanation with research-backed facts]

## Twist/Revelation (4:00-4:30)
[The surprising insight]

## Conclusion (4:30-5:00)
[Wrap-up and call-to-action]

---
**Sources:** [List key sources from research data]

Generate the complete script now:"""

    print("🤖 Generating merged script with Together API...")
    print(f"   Model: meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo")
    
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        messages=[{"role": "user", "content": director_prompt}],
        max_tokens=2500,
        temperature=0.7,
        top_p=0.9,
    )
    
    final_script = response.choices[0].message.content
    print(f"✅ Generated {len(final_script)} characters of merged script")
    
    return final_script

def save_final_script(script, filepath):
    """Save the final merged script to markdown file"""
    print(f"\n💾 Saving final script to {filepath}...")
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(script)
        print(f"✅ Successfully saved final script!")
    except Exception as e:
        print(f"❌ Error saving script: {e}")
        raise

def main():
    """Main execution flow"""
    print("=" * 60)
    print("🎥 VERITASIUM DIRECTOR AGENT")
    print("   Hybrid Fine-Tuning Pipeline + Multi-Agent Research")
    print("=" * 60)
    print()
    
    try:
        # Step 1: Load inputs
        kestra_data = load_kestra_data(KESTRA_OUTPUT)
        finetuned_script = load_finetuned_script(FINETUNED_SCRIPT)
        
        # Step 2: Merge with Director Agent
        final_script = merge_with_director_agent(kestra_data, finetuned_script)
        
        # Step 3: Save output
        save_final_script(final_script, OUTPUT_SCRIPT)
        
        print("\n" + "=" * 60)
        print("✨ SUCCESS! Final script ready for production")
        print(f"📄 Output: {OUTPUT_SCRIPT}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        print("\nPlease ensure:")
        print("  1. test_kestra_output.json exists (run Kestra workflow)")
        print("  2. finetuned_script.txt exists (run inference.py)")
        print("  3. TOGETHER_API_KEY is set in environment")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
