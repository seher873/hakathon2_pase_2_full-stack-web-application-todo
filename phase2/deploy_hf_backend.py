# Deploy Backend to Hugging Face Spaces
# This script uploads the backend to HF Spaces

import os
import sys
from huggingface_hub import HfApi, login

# Configuration
HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_USERNAME = "sehrkhan873"
SPACE_NAME = "HAKATHON-2"
SPACE_ID = f"{HF_USERNAME}/{SPACE_NAME}"

def main():
    if not HF_TOKEN:
        print("❌ HF_TOKEN environment variable not set!")
        print("Get token at: https://huggingface.co/settings/tokens")
        sys.exit(1)
    
    print(f"🚀 Deploying backend to Hugging Face Space: {SPACE_ID}")
    
    # Login
    try:
        login(token=HF_TOKEN)
        print("✅ Logged in to Hugging Face")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        sys.exit(1)
    
    # Initialize API
    api = HfApi()
    
    # Files to upload
    files_to_upload = [
        "app.py",
        "requirements-hf.txt",
    ]
    
    # Upload files
    for file_path in files_to_upload:
        if os.path.exists(file_path):
            print(f"📤 Uploading {file_path}...")
            try:
                api.upload_file(
                    path_or_fileobj=file_path,
                    path_in_repo=file_path,
                    repo_id=SPACE_ID,
                    repo_type="space",
                )
                print(f"✅ Uploaded {file_path}")
            except Exception as e:
                print(f"❌ Failed to upload {file_path}: {e}")
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print("\n✅ Deployment initiated!")
    print(f"📍 Space URL: https://huggingface.co/spaces/{SPACE_ID}")
    print("⏳ Wait a few minutes for the space to rebuild...")

if __name__ == "__main__":
    main()
