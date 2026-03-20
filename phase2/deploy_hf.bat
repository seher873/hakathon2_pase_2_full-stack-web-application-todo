@echo off
REM Hugging Face Spaces Deployment Script
REM For: https://huggingface.co/spaces/sehrkhan873/HAKATHON-2

echo ============================================
echo Hugging Face Spaces Deployment
echo Target: sehrkhan873/HAKATHON-2
echo ============================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

echo [1/4] Checking Git installation...
git --version
echo.

echo [2/4] Adding Hugging Face remote...
git remote remove hf 2>nul
git remote add hf https://huggingface.co/spaces/sehrkhan873/HAKATHON-2.git
echo.

echo [3/4] Pushing to Hugging Face Spaces...
echo This may take a few minutes...
echo.

REM Push to Hugging Face
git push -u hf main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo SUCCESS! Deployment initiated.
    echo ============================================
    echo.
    echo Your Space will be available at:
    echo https://huggingface.co/spaces/sehrkhan873/HAKATHON-2
    echo.
    echo Build time: 5-10 minutes
    echo Check the Space page for build progress.
    echo.
) else (
    echo.
    echo ============================================
    echo ERROR: Push failed!
    echo ============================================
    echo.
    echo Possible issues:
    echo 1. Not authenticated with Hugging Face
    echo 2. Space does not exist
    echo 3. Network connection issue
    echo.
    echo To authenticate, run:
    echo huggingface-cli login
    echo.
    echo Or create a token at:
    echo https://huggingface.co/settings/tokens
    echo.
)

pause
