# Hugging Face Spaces Deployment Script
# For: https://huggingface.co/spaces/sehrkhan873/HAKATHON-2

import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and print status."""
    print(f"\n{'='*50}")
    print(f"📦 {description}")
    print(f"{'='*50}")
    print(f"Command: {cmd}\n")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    return result.returncode == 0

def main():
    print("\n" + "="*60)
    print("🤗 Hugging Face Spaces Deployment")
    print("📍 Target: sehrkhan873/HAKATHON-2")
    print("="*60)
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    print(f"\n📁 Working directory: {project_dir}")
    
    # Step 1: Check Git
    if not run_command("git --version", "Checking Git installation"):
        print("❌ Git is not installed!")
        return False
    
    # Step 2: Stage all changes
    if not run_command("git add -A", "Staging all changes"):
        print("❌ Failed to stage changes!")
        return False
    
    # Step 3: Commit
    if not run_command('git commit -m "Deploy to Hugging Face Spaces"', "Committing changes"):
        print("ℹ️  No changes to commit or commit failed")
    
    # Step 4: Add/Update HF remote
    print("\n" + "="*50)
    print("🔗 Configuring Hugging Face remote")
    print("="*50)
    
    # Remove existing hf remote if any
    subprocess.run("git remote remove hf 2>$null", shell=True)
    
    hf_url = "https://huggingface.co/spaces/sehrkhan873/HAKATHON-2.git"
    run_command(f'git remote add hf {hf_url}', "Adding Hugging Face remote")
    
    # Step 5: Verify remote
    print("\n" + "="*50)
    print("📋 Current remotes:")
    print("="*50)
    run_command("git remote -v", "Listing remotes")
    
    # Step 6: Push to HF
    print("\n" + "="*50)
    print("🚀 Pushing to Hugging Face Spaces...")
    print("="*50)
    print("⚠️  You may be prompted for credentials.")
    print("💡 Use your Hugging Face token as password.")
    print("📍 Get token at: https://huggingface.co/settings/tokens\n")
    
    success = run_command("git push hf main", "Pushing to Hugging Face")
    
    if success:
        print("\n" + "="*60)
        print("✅ SUCCESS!")
        print("="*60)
        print("\n🌐 Your Space will be available at:")
        print("   https://huggingface.co/spaces/sehrkhan873/HAKATHON-2")
        print("\n⏱️  Build time: 5-10 minutes")
        print("📊 Check build progress on the Space page")
        print("\n🔧 To update in future:")
        print("   git push hf main")
        print("="*60 + "\n")
    else:
        print("\n" + "="*60)
        print("❌ Deployment failed!")
        print("="*60)
        print("\nPossible solutions:")
        print("1. Authenticate with HF CLI:")
        print("   pip install huggingface_hub")
        print("   huggingface-cli login")
        print("\n2. Or use a token:")
        print("   - Go to: https://huggingface.co/settings/tokens")
        print("   - Create a new token (write access)")
        print("   - Use it as password when pushing")
        print("\n3. Manual deploy:")
        print("   git clone https://huggingface.co/spaces/sehrkhan873/HAKATHON-2")
        print("   Copy files and push")
        print("="*60 + "\n")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
