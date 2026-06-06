@echo off
REM =============================================
REM  Knowledge Updater - Windows Task Scheduler
REM =============================================
REM  Schedule: Weekly, Monday 06:00
REM  Usage:    Run this via Windows Task Scheduler
REM  Log:      Output appended to crawl_log.txt
REM =============================================

set SKILL_DIR=D:\affiliate-content-creator-skill
set LOG_FILE=%SKILL_DIR%\tools\crawl_log.txt

echo [%DATE% %TIME%] Starting knowledge crawl... >> "%LOG_FILE%"

cd /d "%SKILL_DIR%"

REM Run the Python crawler
python tools\knowledge_updater.py --topic "affiliate marketing TikTok Shop" >> "%LOG_FILE%" 2>&1

REM Check exit code
if %ERRORLEVEL% EQU 0 (
    echo [%DATE% %TIME%] Crawl completed successfully >> "%LOG_FILE%"
) else (
    echo [%DATE% %TIME%] Crawl FAILED with error code %ERRORLEVEL% >> "%LOG_FILE%"
)

echo ---------------------------------------- >> "%LOG_FILE%"
