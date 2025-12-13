import asyncio
import edge_tts
import os
import sys
import requests
import json
import time
import argparse
from dotenv import load_dotenv

# Try to import ElevenLabs, handle if missing
try:
    from elevenlabs import ElevenLabs
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    print("⚠️ ElevenLabs library not found. Install with: pip install elevenlabs")

# Load environment variables
load_dotenv()

# API Keys
WAVESPEED_API_KEY = os.environ.get("WAVESPEED_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# Configuration
IMAGE_PATH = "face/veritasium_dreamworks.png"
AUDIO_DIR_NAME = "generated_tts"
VIDEO_DIR_NAME = "generated_video"

async def generate_audio_edge_tts(text_file, output_file, debug=False):
    """Generate audio using Edge TTS (Free fallback)"""
    try:
        with open(text_file, 'r', encoding='utf-8') as f:
            script_text = f.read()
    except Exception as e:
        raise FileNotFoundError(f"Could not read text file: {text_file}. Error: {e}")

    print(f"🎵 Generating audio (Edge TTS) from {text_file}...")
    if debug:
        print(f"DEBUG: Script text preview: {script_text[:200]}...")
    
    communicate = edge_tts.Communicate(script_text, "en-AU-WilliamNeural")
    await communicate.save(output_file)
    
    if debug:
        if os.path.exists(output_file):
            print(f"DEBUG: Audio saved, file size: {os.path.getsize(output_file)} bytes")
        else:
            print("DEBUG: Audio file was NOT saved correctly.")

    print(f"✅ Audio saved to {output_file}")
    return output_file

def generate_audio_elevenlabs(text_file, output_file, debug=False):
    """Generate audio using ElevenLabs (High Quality)"""
    if not ELEVENLABS_AVAILABLE:
        raise ImportError("ElevenLabs package not installed.")

    if not ELEVENLABS_API_KEY:
        raise ValueError("❌ ELEVENLABS_API_KEY not found in environment or .env file")

    try:
        with open(text_file, 'r', encoding='utf-8') as f:
            script_text = f.read()
    except Exception as e:
        raise FileNotFoundError(f"Could not read text file: {text_file}. Error: {e}")

    print(f"🎵 Generating audio (ElevenLabs) from {text_file}...")
    if debug:
        print(f"DEBUG: Script text preview: {script_text[:200]}...")
    
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    voice_id = "FRfK9ktUgII8Yh5EUCn1"  # Derek Muller style

    try:
        # Voice Settings
        voice_settings = {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.5,
            "use_speaker_boost": True
        }
        
        # Generate audio
        # Using 'eleven_multilingual_v2' as it is generally available on free tiers/standard plans
        audio_generator = client.text_to_speech.convert(
            voice_id=voice_id,
            text=script_text,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
            voice_settings=voice_settings
        )
        
        # Save to file
        with open(output_file, 'wb') as f:
            for chunk in audio_generator:
                f.write(chunk)
        
        if debug:
            print(f"DEBUG: Audio saved, file size: {os.path.getsize(output_file)} bytes")
        print(f"✅ Audio saved to {output_file}")
        return output_file

    except Exception as e:
        print(f"❌ ElevenLabs API Error: {e}")
        raise

def upload_file_to_public_host(file_path, debug=False):
    """Upload file to a free public host (file.io)"""
    upload_url = "https://file.io"
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            # Expires after 1 download or 2 weeks to respect privacy/limits
            response = requests.post(upload_url, files=files, data={"expires": "2w"}, timeout=30)
        
        if debug:
            print(f"DEBUG: Public upload status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if not data.get("success"):
                 raise Exception(f"File.io error: {data}")
            return data["link"]
        else:
            raise Exception(f"Public upload failed (status {response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ Public upload error: {e}")
        raise

def generate_video_wavespeed(audio_url, image_url, debug=False):
    """Generate video using WaveSpeed AI API"""
    if not WAVESPEED_API_KEY:
        raise ValueError("WAVESPEED_API_KEY is missing.")

    generate_url = "https://api.wavespeed.ai/api/v3/wavespeed-ai/hunyuan-avatar"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WAVESPEED_API_KEY}",
    }
    payload = {
        "audio": audio_url,
        "image": image_url,
        "resolution": "480p"
    }
    
    print("🎬 Starting WaveSpeed video generation...")
    if debug:
        print(f"DEBUG: WaveSpeed Payload: {payload}")
    
    begin = time.time()
    response = requests.post(generate_url, headers=headers, data=json.dumps(payload), timeout=30)
    
    if response.status_code != 200:
        raise Exception(f"WaveSpeed request failed (status {response.status_code}): {response.text}")
    
    result = response.json().get("data", {})
    request_id = result.get("id")
    if not request_id:
         raise Exception(f"No Request ID returned. Response: {response.text}")

    print(f"Task submitted successfully. Request ID: {request_id}")
    
    # Poll for results
    poll_url = f"https://api.wavespeed.ai/api/v3/predictions/{request_id}/result"
    headers = {"Authorization": f"Bearer {WAVESPEED_API_KEY}"}
    
    while True:
        response = requests.get(poll_url, headers=headers, timeout=30)
        if response.status_code != 200:
            raise Exception(f"Poll failed (status {response.status_code}): {response.text}")
        
        result = response.json().get("data", {})
        status = result.get("status")
        
        if status == "completed":
            end = time.time()
            print(f"Task completed in {end - begin:.1f} seconds.")
            outputs = result.get("outputs", [])
            if outputs:
                video_url = outputs[0]
                print(f"✅ Video generated: {video_url}")
                return video_url
            else:
                 raise Exception("Completed but no output video found.")
        elif status == "failed":
            raise Exception(result.get("error", "Generation failed"))
        else:
            if debug:
                print(f"⏳ Status: {status}... Waiting 2s")
            time.sleep(2)

def download_video_from_url(video_url, output_file, debug=False):
    """Download video from URL"""
    print(f"📥 Downloading video from {video_url}...")
    response = requests.get(video_url, stream=True)
    response.raise_for_status()
    
    with open(output_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    
    print(f"✅ Downloaded video to {output_file}")
    return output_file

def generate_video_pipeline(script_file, tts_engine="elevenlabs", debug=False):
    """
    Main orchestration function.
    FIXED: Explicit check for tts.txt - abort if not found to save API credits
    """
    # FIXED: Check if tts.txt exists - if not, abort early
    tts_file = "../research_outputs/tts.txt"
    if not os.path.exists(tts_file):
        print(f"❌ TTS file not found: {tts_file}")
        print("Video generation aborted to avoid API usage. Run pipeline first to generate tts.txt.")
        sys.exit(1)  # Exit to prevent any API calls

    script_file = tts_file  # Use tts.txt as input for TTS/video

    # 1. Setup Directories (Relative to this script location)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    audio_dir = os.path.join(base_dir, AUDIO_DIR_NAME)
    video_dir = os.path.join(base_dir, VIDEO_DIR_NAME)
    
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(video_dir, exist_ok=True)

    # 2. Generate TTS Audio
    output_filename = "output.mp3"
    audio_file = os.path.join(audio_dir, output_filename)

    if tts_engine == "elevenlabs":
        audio_file = generate_audio_elevenlabs(script_file, audio_file, debug=debug)
    elif tts_engine == "edge_tts":
        audio_file = asyncio.run(generate_audio_edge_tts(script_file, audio_file, debug=debug))
    else:
        raise ValueError("Unknown TTS engine")

    # 3. Generate Video (Only if key exists)
    if WAVESPEED_API_KEY:
        try:
            # Upload assets
            print("📤 Uploading assets for video generation...")
            audio_url = upload_file_to_public_host(audio_file, debug=debug)
            
            # Check for image file
            # Looks for image in 'face' folder relative to script or CWD
            possible_image_paths = [
                os.path.join(base_dir, IMAGE_PATH),
                IMAGE_PATH,
                os.path.abspath(IMAGE_PATH)
            ]
            
            real_image_path = None
            for p in possible_image_paths:
                if os.path.exists(p):
                    real_image_path = p
                    break
            
            if not real_image_path:
                print(f"⚠️ Image not found at {IMAGE_PATH}. Skipping video generation.")
                return audio_file

            image_url = upload_file_to_public_host(real_image_path, debug=debug)
            
            # Generate Video
            video_url = generate_video_wavespeed(audio_url, image_url, debug=debug)
            
            # Download Video
            video_filename = f"generated_video_{int(time.time())}.mp4"
            local_video_path = os.path.join(video_dir, video_filename)
            download_video_from_url(video_url, local_video_path, debug=debug)
            
            return local_video_path

        except Exception as e:
            print(f"⚠️ Video generation failed (returning audio only): {e}")
            return audio_file
    else:
        print("⚠️ WAVESPEED_API_KEY not found. Skipping video generation.")
        return audio_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--tts", default="elevenlabs", choices=["elevenlabs", "edge_tts"], help="TTS engine to use")
    parser.add_argument("--file", type=str, help="Path to specific text file", default=None)
    args = parser.parse_args()

    # Define the specific file you want to use
    specific_filename = "tts.txt"

    # Search Logic: 
    # 1. User provided argument
    # 2. Specific filename in research_outputs (relative to root)
    # 3. Specific filename in research_outputs (relative to script dir)

    target_file = None

    if args.file and os.path.exists(args.file):
        target_file = args.file
    else:
        possible_paths = [
            # Check research_outputs folder from root
            os.path.join("research_outputs", specific_filename),
            # Check relative to script location if script is run from inside ai-engine
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "research_outputs", specific_filename),
            # Fallback
            specific_filename
        ]
        
        for p in possible_paths:
            if os.path.exists(p):
                target_file = p
                break

    if target_file:
        print(f"📄 Processing file: {target_file}")
        output = generate_video_pipeline(target_file, tts_engine=args.tts, debug=args.debug)
        print(f"🎉 Final Output: {output}")
    else:
        print(f"❌ Error: Could not find input file: '{specific_filename}'")
        print("   Video generation aborted to save API credits.")