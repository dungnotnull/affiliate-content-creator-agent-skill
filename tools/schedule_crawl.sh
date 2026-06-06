#!/usr/bin/env bash
# =============================================
#  Knowledge Updater - Unix/Linux cron wrapper
# =============================================
#  Crontab entry (run weekly on Monday 06:00):
#    0 6 * * 1 /path/to/schedule_crawl.sh
# =============================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_FILE="${SKILL_DIR}/tools/crawl_log.txt"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting knowledge crawl..." >> "${LOG_FILE}"

cd "${SKILL_DIR}"

# Run the Python crawler with default topic
python3 tools/knowledge_updater.py --topic "affiliate marketing TikTok Shop" >> "${LOG_FILE}" 2>&1

EXIT_CODE=$?
if [ ${EXIT_CODE} -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Crawl completed successfully" >> "${LOG_FILE}"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Crawl FAILED with error code ${EXIT_CODE}" >> "${LOG_FILE}"
fi

echo "----------------------------------------" >> "${LOG_FILE}"
