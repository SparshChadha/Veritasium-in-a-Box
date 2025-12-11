import json
import re
import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

CHANNEL_ID = "UCHnyfMqiRRG1u-2MsSQLbXA"
OUTPUT_FILE = "veritasium_train.jsonl"
LIMIT = 50

def clean_text(text):
    # Remove bracketed sounds like [Music], [Applause], [Laughter]
    """
    Remove bracketed annotations (e.g., "[Music]", "[Applause]", "[Laughter]") from a transcript string.
    
    Parameters:
        text (str): Input text that may contain bracketed annotations.
    
    Returns:
        str: The input string with bracketed content removed and leading/trailing whitespace trimmed.
    """
    return re.sub(r'\[.*?\]', '', text).strip()

def fetch_data():
    """
    Fetches recent videos from the configured YouTube channel, extracts and cleans transcripts, and writes them as Oumi SFT-style JSONL records.
    
    Each output record is a JSON object with a "messages" array: a user prompt "Write a script for: <title>" and an assistant message containing the cleaned transcript. The function uses CHANNEL_ID and LIMIT to select videos, writes one JSON object per line to OUTPUT_FILE, performs network I/O to retrieve transcripts, logs progress to stdout, and skips videos whose transcripts cannot be obtained.
    """
    print(f"Fetching last {LIMIT} videos from channel {CHANNEL_ID}...")
    videos = scrapetube.get_channel(CHANNEL_ID, limit=LIMIT)
    
    data = []
    
    for video in videos:
        video_id = video['videoId']
        # title is sometimes nested or simple string depending on scrapetube version/response
        # scrapetube usually returns a dict with 'title' as a dict with 'runs' or just 'simpleText'
        # simpler to just trust the key structure or use a safe get
        try:
            title = video['title']['runs'][0]['text']
        except (KeyError, IndexError, TypeError):
             # Fallback for different response structures
            title = video.get('title', {}).get('simpleText', f"Video {video_id}")

        print(f"Processing: {title} ({video_id})")
        
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            formatter = TextFormatter()
            transcript_text = formatter.format_transcript(transcript_list)
            
            # Clean the transcript
            cleaned_transcript = clean_text(transcript_text)
            
            # Oumi SFT chat format
            entry = {
                "messages": [
                    {"role": "user", "content": f"Write a script for: {title}"},
                    {"role": "assistant", "content": cleaned_transcript}
                ]
            }
            data.append(entry)
            
        except Exception as e:
            print(f"Failed to get transcript for {video_id}: {e}")
            continue

    print(f"Saving {len(data)} records to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for entry in data:
            json.dump(entry, f)
            f.write('\n')
    
    print("Done!")

if __name__ == "__main__":
    fetch_data()

