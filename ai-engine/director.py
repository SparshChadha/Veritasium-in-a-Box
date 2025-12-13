#!/usr/bin/env python3
"""
Director Agent - Merges Kestra research data with fine-tuned script output
Uses Cerebras API (Llama 3.1 70B) to create a cohesive 5-minute Veritasium-style script
"""
import json
import os
import subprocess
import sys
import argparse
from dotenv import load_dotenv
load_dotenv()  # This loads variables from .env into os.environ

try:
    from cerebras.cloud.sdk import Cerebras
except ImportError:
    print("❌ Error: Cerebras SDK not found.")
    print(" Please run: pip install cerebras_cloud_sdk")
    exit(1)

# Configuration
MODEL_ID = "llama3.1-8b"
KESTRA_OUTPUT = "research_outputs/kestra_output.json"  # Path from project root
FINETUNED_SCRIPT = "research_outputs/finetuned_script.txt"  # Path from project root
OUTPUT_SCRIPT = "research_outputs/final_5min_script.md"

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
        print(" Please ensure the Kestra workflow or generate_kestra_output.py has generated the data.")
        print(" Expected location: research_outputs/kestra_output.json")
        raise
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {filepath}: {e}")
        raise

def generate_draft(topic):
    """Run generate_draft.py to create fine-tuned script."""
    print(f"📝 Generating draft script for topic: {topic}...")
    cmd = ["python3", "generate_draft.py", "--topic", topic]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd="fine_tuned_model")  # Run in fine_tuned_model dir
    if result.returncode != 0:
        print(f"❌ Draft generation failed: {result.stderr}")
        raise RuntimeError("Draft generation failed")
    print("✅ Draft generated: research_outputs/finetuned_script.txt")
    return FINETUNED_SCRIPT  # Return path to loaded file

def load_finetuned_script(filepath):
    """Load fine-tuned model script output (called after generate_draft)."""
    print(f"📝 Loading fine-tuned script from {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            script = f.read()
        print(f"✅ Loaded {len(script)} characters of script content")
        return script
    except FileNotFoundError:
        print(f"❌ Error: {filepath} not found")
        print(" Please run generate_draft.py from the fine_tuned_model directory first.")
        raise

def merge_with_director_agent(kestra_data, finetuned_script):
    """
    Use Cerebras API (Director Agent) to merge research and script
    Creates a cohesive 5-minute Veritasium-style video script
    """
    print("\n🎬 Activating Director Agent (Cerebras AI)...")
  
    # Get API key from environment
    api_key = os.environ.get("CEREBRAS_API_KEY")
    if not api_key:
        raise ValueError(
            "❌ CEREBRAS_API_KEY environment variable not set!\n"
            " Please set it: export CEREBRAS_API_KEY='your-api-key'"
        )
  
    client = Cerebras(api_key=api_key)
  
    # Format the research data for the prompt
    kestra_summary = json.dumps(kestra_data, indent=2)
  
    # Create the director prompt (FIXED: Escaped braces, complete f-string)
    director_prompt = f"""You are a Director Agent for creating Veritasium-style educational video scripts.Your task: Merge research data from a multi-agent system (Kestra) with a draft script from a fine-tuned Llama model to create a polished, engaging 5-minute video script.

    **RESEARCH DATA (from Kestra Multi-Agent System):**
    ```json
    {{kestra_summary}}
    DRAFT SCRIPT (from Fine-Tuned Veritasium Model):
    {finetuned_script}

    YOUR MISSION:
    Create a final 5-minute Veritasium-style video script that:

    Integrates key facts from the research data into the narrative
    Maintains the style and flow from the fine-tuned script
    Adds scientific accuracy using the research citations
    Structures for engagement: Hook → Explanation → Twist/Revelation → Conclusion
    Targets 5 minutes of speaking time (~750 words)
    OUTPUT FORMAT (Markdown):

    [Compelling Title]
    Hook (0:00-0:30)
    [Opening that grabs attention]
    Main Content (0:30-4:00)
    [Core explanation with research-backed facts]
    Twist/Revelation (4:00-4:30)
    [The surprising insight]
    Conclusion (4:30-5:00)
    [Wrap-up and call-to-action]
    Sources: [List key sources from research data]
    Generate the complete script now:
"""
    
    print("🤖 Generating merged script with Cerebras (Llama 3.1 70B)...")
    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": director_prompt}],
            max_tokens=2500,
            temperature=0.7,
            top_p=0.9,
        )
        final_script = response.choices[0].message.content
        print(f"✅ Generated {len(final_script)} characters of merged script")
        return final_script
    except Exception as e:
        print(f"❌ Cerebras API Error: {str(e)}")
        raise

def save_final_script(script, filepath):
    """Save the final merged script and create clean TTS text file"""
    print(f"\n💾 Processing final script...")

    try:
        # FIXED: Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Save the markdown version
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(script)
        print(f"✅ Saved markdown script: {filepath}")

        # Extract title and create clean TTS text
        lines = script.split('\n')
        title = ""
        tts_content = []

        # Find title (first line with **title** that doesn't contain timing info or colons)
        for line in lines:
            line_stripped = line.strip()
            if (line_stripped.startswith('**') and line_stripped.endswith('**') and
                not any(char in line_stripped for char in ['(', ')', ':00', ':30']) and
                'Title:' not in line_stripped and 'title:' not in line_stripped):
                title = line_stripped.strip('**').strip()
                break

        # Fallback: look for title in quotes if no clean title found
        if not title:
            for line in lines:
                if '"' in line and ('Title' in line or 'title' in line):
                    # Extract text between quotes
                    start = line.find('"')
                    end = line.find('"', start + 1)
                    if start != -1 and end != -1:
                        title = line[start+1:end]
                        break

        if not title:
            title = "Veritasium_Script"

        # Extract clean script content (skip headers and sources)
        skip_sources = False
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Stop processing when we reach sources section
            if 'Sources' in line or 'sources' in line or '[1]' in line or 'Annals' in line:
                skip_sources = True
                continue

            if skip_sources:
                continue

            # Skip title line
            if line.startswith('**') and line.endswith('**') and not any(char in line for char in ['(', ')', ':00', ':30']):
                continue

            # Skip section headers (both ** and ### formats)
            if (line.startswith('**') or line.startswith('###')) and (
                'Hook' in line or 'Main Content' in line or 'Twist' in line or
                'Conclusion' in line or 'Note:' in line
            ):
                continue

            # Skip timing labels in parentheses
            if ('0:00' in line or '0:30' in line or '4:00' in line or '4:30' in line or '5:00' in line):
                continue

            # Skip any remaining header-like lines
            if line.startswith('### ') or line.startswith('**') or line.startswith('* ') or line.startswith('['):
                continue

            # Add actual content lines (skip very short lines)
            if line and len(line) > 15:  # Only keep substantial content lines
                tts_content.append(line)

        # Create clean TTS text file
        clean_script = '\n\n'.join(tts_content)
        tts_filepath = "research_outputs/tts.txt"

        with open(tts_filepath, 'w', encoding='utf-8') as f:
            f.write(clean_script)

        print(f"✅ Saved TTS-ready script: {tts_filepath}")

    except Exception as e:
        print(f"❌ Error saving scripts: {e}")
        raise

def main():
    """Main execution flow"""
    parser = argparse.ArgumentParser(description="Veritasium Director Agent")
    parser.add_argument("--topic", default="Default topic", help="Video topic for context")
    args = parser.parse_args()

    print("=" * 60)
    print("🎥 VERITASIUM DIRECTOR AGENT (Powered by Cerebras)")
    print(" Hybrid Fine-Tuning Pipeline + Multi-Agent Research")
    print("=" * 60)
    print()

    try:
        # Step 1: Load inputs
        kestra_data = load_kestra_data(KESTRA_OUTPUT)

        # Check if finetuned_script.txt already exists
        if os.path.exists(FINETUNED_SCRIPT):
            print(f"✅ Found existing {FINETUNED_SCRIPT}, using it directly...")
            finetuned_script = load_finetuned_script(FINETUNED_SCRIPT)
        else:
            # Generate draft script if file doesn't exist
            generate_draft(args.topic)  # Runs generate_draft.py from fine_tuned_model directory
            finetuned_script = load_finetuned_script(FINETUNED_SCRIPT)  # Loads after generate_draft call
        # Step 2: Merge with Director Agent
        final_script = merge_with_director_agent(kestra_data, finetuned_script)
        # Step 3: Save output
        save_final_script(final_script, OUTPUT_SCRIPT)
        print("\n" + "=" * 60)
        print("✨ SUCCESS! Final script ready for production")
        print("📄 Files saved to research_outputs/ folder")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        print("\nPlease ensure:")
        print(" 1. research_outputs/kestra_output.json exists (run Kestra workflow or generate_kestra_output.py)")
        print(" 2. generate_draft.py exists in fine_tuned_model/ directory")
        print(" 3. CEREBRAS_API_KEY is set in environment")
        return 1
    return 0

if __name__ == "__main__":  # FIXED: Corrected typo
    exit(main())