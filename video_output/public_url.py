import os
import requests

# Path to your local image
LOCAL_IMAGE = "/Users/sparsh/veritasium in a box 2/Veritasium-in-a-Box/video_output/face/veritasium_dreamworks.png"

def upload_image_to_0x0_st(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None
    
    upload_url = "https://0x0.st"
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        response = requests.post(upload_url, files=files)
    
    if response.status_code == 200:
        # 0x0.st returns a direct link (e.g., https://0x0.st/XYZ.png)
        public_url = response.text.strip()
        print(f"✅ Uploaded successfully!\nPublic URL: {public_url}")
        return public_url
    else:
        print(f"❌ Upload failed: {response.status_code}\n{response.text}")
        return None

if __name__ == "__main__":
    upload_image_to_0x0_st(LOCAL_IMAGE)
