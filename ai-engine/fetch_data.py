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
    return re.sub(r'\[.*?\]', '', text).strip()

def fetch_data():
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


