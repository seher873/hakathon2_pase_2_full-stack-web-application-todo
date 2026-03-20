#!/usr/bin/env python3
"""
Hugging Face Spaces Deployment Script
Uses huggingface_hub CLI for deployment

Git User: seher873
HF User: sehrkhan873
Target: https://huggingface.co/spaces/sehrkhan873/HAKATHON-2
"""

import os
import subprocess
import sys

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_cmd(cmd, show_output=True):
    """Run command and return success status."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        if show_output and result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print_header("Hugging Face Spaces Deployment")
    print("Git User: seher873")
    print("HF User: sehrkhan873")
    print("Target: sehrkhan873/HAKATHON-2")
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"\nWorking directory: {script_dir}\n")
    
    # Step 1: Install huggingface_hub
    print_header("Step 1: Installing huggingface_hub")
    run_cmd("py -m pip install huggingface_hub -q")
    print("✓ huggingface_hub installed")
    
    # Step 2: Login
    print_header("Step 2: Hugging Face Authentication")
    print("Please enter your Hugging Face token:")
    print("Get one at: https://huggingface.co/settings/tokens\n")
    run_cmd("py -c \"from huggingface_hub import login; login()\"")
    
    # Step 3: Git config
    print_header("Step 3: Git Configuration")
    run_cmd("git config user.name \"seher873\"")
    run_cmd("git config user.email \"seher873@users.noreply.huggingface.co\"")
    print("✓ Git user configured")
    
    # Step 4: Stage changes
    print_header("Step 4: Staging Changes")
    run_cmd("git add -A")
    print("✓ Changes staged")
    
    # Step 5: Commit
    print_header("Step 5: Committing Changes")
    run_cmd('git commit -m "Deploy to Hugging Face Spaces"')
    
    # Step 6: Add HF remote
    print_header("Step 6: Setting up Hugging Face Remote")
    run_cmd("git remote remove hf")
    hf_url = "https://huggingface.co/spaces/sehrkhan873/HAKATHON-2.git"
    run_cmd(f'git remote add hf {hf_url}')
    print(f"✓ Remote added: {hf_url}")
    
    # Step 7: Verify remote
    print_header("Step 7: Verifying Remote")
    run_cmd("git remote -v")
    
    # Step 8: Push to HF
    print_header("Step 8: Pushing to Hugging Face Spaces")
    print("⚠️  This may take a few minutes...")
    print("⚠️  You may be prompted for credentials\n")
    
    success = run_cmd("git push -u hf main")
    
    if success:
        print_header("SUCCESS!")
        print("✅ Deployment initiated!")
        print("\n🌐 Your Space:")
        print("   https://huggingface.co/spaces/sehrkhan873/HAKATHON-2")
        print("\n⏱️  Build time: 5-10 minutes")
        print("📊 Check progress on the Space page")
        print("\n🔧 To update later:")
        print("   git push hf main")
    else:
        print_header("Deployment Failed")
        print("❌ Push failed!")
        print("\nSolutions:")
        print("1. Get a token: https://huggingface.co/settings/tokens")
        print("2. Run: huggingface-cli login")
        print("3. Try again: git push hf main")
    
    print("\n" + "="*60 + "\n")
    return success

if __name__ == "__main__":
    try:
        success = main()
        input("Press Enter to exit...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
