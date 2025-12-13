#!/usr/bin/env python3
"""
Veritasium Content Generation Pipeline

This pipeline orchestrates the complete process:
1. Research generation (Kestra CLI or local fallback)
2. Script drafting (fine-tuned model)
3. Final script creation (Director Agent)

All outputs are saved to research_outputs/ folder.
"""
import subprocess
import argparse
import os
from slugify import slugify  # Still needed for Kestra CLI path
import time

def run_kestra(topic):
    """Run Kestra workflow via CLI, fallback to local script if unavailable."""
    print(f"🔬 Running Kestra research for '{topic}'...")

    # Try Kestra CLI first
    cmd = ["kestra", "flow", "run", "dev.multi-agent-research", "-i", f"topic={topic}"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Kestra complete—JSON in research_outputs/")
        return f"research_outputs/{slugify(topic)}_research.json"
    else:
        print(f"⚠️  Kestra CLI not available: {result.stderr}")
        print("🔄 Falling back to local generate_kestra_output.py...")

        # Fallback to local script
        fallback_cmd = ["python3", "../kestra/generate_kestra_output.py", topic]
        fallback_result = subprocess.run(fallback_cmd, capture_output=True, text=True, cwd=".")

        if fallback_result.returncode != 0:
            raise RuntimeError(f"Both Kestra and fallback failed. Kestra: {result.stderr}, Fallback: {fallback_result.stderr}")

        print("✅ Local research complete—JSON in research_outputs/")
        return "research_outputs/kestra_output.json"

def generate_draft(topic):
    """Run fine-tuned model from fine_tuned_model directory."""
    print(f"📝 Generating draft script...")
    subprocess.run(["python3", "generate_draft.py", "--topic", topic], check=True, cwd="../fine_tuned_model")
    return "research_outputs/finetuned_script.txt"

def merge_final(kestra_json, draft_file):
    """Run director to create final outputs in research_outputs."""
    print("🎬 Merging with Director Agent...")
    subprocess.run(["python3", "director.py"], check=True)  # Outputs to research_outputs/
    return "research_outputs/final_5min_script.md"

def main():
    parser = argparse.ArgumentParser(description="Veritasium Pipeline")
    parser.add_argument("--topic", required=True, help="Video topic")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    
    kestra_json = run_kestra(args.topic)
    draft_file = generate_draft(args.topic)
    final_script = merge_final(kestra_json, draft_file)
    
    print(f"✨ Pipeline complete! Final outputs in research_outputs/ folder:")
    print(f"   📄 {final_script}")
    print(f"   🗣️  research_outputs/tts.txt")

if __name__ == "__main__":
    main()