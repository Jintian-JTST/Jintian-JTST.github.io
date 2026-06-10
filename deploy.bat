@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo  Deploy site to GitHub Pages
echo  Repo: Jintian-JTST/Jintian-JTST.github.io
echo ============================================
echo.

where git >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Git not found. Install it from https://git-scm.com/download/win
    pause
    exit /b 1
)

if not exist ".git" (
    echo [1/4] Initializing git repository...
    git init
    git branch -M main
    git remote add origin https://github.com/Jintian-JTST/Jintian-JTST.github.io.git
) else (
    echo [1/4] Git repository already initialized.
    git remote get-url origin >nul 2>nul
    if errorlevel 1 git remote add origin https://github.com/Jintian-JTST/Jintian-JTST.github.io.git
)

echo [2/4] Staging all files...
git add -A

echo [3/4] Committing...
git commit -m "Update site: fill in project pages, add new projects"
if errorlevel 1 echo (Nothing new to commit, continuing...)

echo [4/4] Pushing to GitHub...
git push -u origin main
if errorlevel 1 (
    echo.
    echo [ERROR] Push failed. Most common reasons:
    echo   1. The repo doesn't exist yet - create it at:
    echo      https://github.com/new
    echo      Name it EXACTLY: Jintian-JTST.github.io  (Public, no README)
    echo   2. Not logged in - a browser window should pop up to sign in.
    echo   3. Remote has commits you don't have locally. To overwrite, run:
    echo      git push -u origin main --force
    pause
    exit /b 1
)

echo.
echo ============================================
echo  Done! Your site will be live in ~1 minute:
echo  https://jintian-jtst.github.io
echo ============================================
pause
