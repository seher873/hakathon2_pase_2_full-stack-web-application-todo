@echo off
REM ============================================
REM Hugging Face Spaces Deployment Script
REM ============================================
REM Git Username: seher873
REM HF Username: sehrkhan873
REM Target: https://huggingface.co/spaces/sehrkhan873/HAKATHON-2
REM ============================================

echo.
echo ============================================
echo   Hugging Face Spaces Deployment
echo ============================================
echo.
echo   Git User: seher873
echo   HF User:  sehrkhan873
echo   Target:   sehrkhan873/HAKATHON-2
echo ============================================
echo.

cd /d "%~dp0"

REM Step 1: Install huggingface_hub if needed
echo [1/6] Checking huggingface_hub installation...
py -c "import huggingface_hub" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing huggingface_hub...
    py -m pip install huggingface_hub -q
)
echo Done!
echo.

REM Step 2: Login to Hugging Face
echo [2/6] Hugging Face Authentication
echo ============================================
echo Please enter your Hugging Face token when prompted.
echo Get a token at: https://huggingface.co/settings/tokens
echo ============================================
echo.
py -m pip install huggingface_hub -q
py -c "from huggingface_hub import login; login()"
echo.

REM Step 3: Git configuration
echo [3/6] Configuring Git...
git config user.name "seher873"
git config user.email "seher873@users.noreply.huggingface.co"
echo Git user set to: seher873
echo.

REM Step 4: Stage and commit changes
echo [4/6] Staging and committing changes...
git add -A
git commit -m "Deploy to Hugging Face Spaces - AI Todo App"
echo.

REM Step 5: Add Hugging Face remote
echo [5/6] Setting up Hugging Face remote...
git remote remove hf 2>nul
git remote add hf https://huggingface.co/spaces/sehrkhan873/HAKATHON-2.git
echo Remote added: hf
echo.

REM Step 6: Push to Hugging Face
echo [6/6] Pushing to Hugging Face Spaces...
echo ============================================
echo This may take a few minutes...
echo ============================================
echo.
git push -u hf main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo   SUCCESS!
    echo ============================================
    echo.
    echo   Your Space is deploying at:
    echo   https://huggingface.co/spaces/sehrkhan873/HAKATHON-2
    echo.
    echo   Build time: 5-10 minutes
    echo   Check the Space page for progress.
    echo.
    echo   To update later, run:
    echo   git push hf main
    echo.
) else (
    echo.
    echo ============================================
    echo   ERROR: Push failed!
    echo ============================================
    echo.
    echo   Possible solutions:
    echo   1. Make sure you have a valid HF token
    echo   2. Check that the Space exists:
    echo      https://huggingface.co/spaces/sehrkhan873/HAKATHON-2
    echo   3. Create the Space first if it doesn't exist
    echo.
)

echo ============================================
pause
