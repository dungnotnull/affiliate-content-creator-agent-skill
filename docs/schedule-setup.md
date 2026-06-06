# Schedule Setup — Knowledge Updater

This document explains how to schedule the `tools/knowledge_updater.py` script to run weekly (Monday 06:00) so the `SECOND-KNOWLEDGE-BRAIN.md` stays current with the latest affiliate marketing data.

---

## Windows (Task Scheduler)

1. Open **Task Scheduler** (Win+R → `taskschd.msc`)
2. Click **Create Task...** in the Actions panel
3. **General** tab:
   - Name: `AffiliateContentCreator-KnowledgeUpdate`
   - Description: `Weekly crawl of affiliate marketing news → SECOND-KNOWLEDGE-BRAIN.md`
   - Check **Run whether user is logged on or not**
   - Check **Run with highest privileges**
4. **Triggers** tab → **New...**:
   - Begin the task: `On a schedule`
   - Settings: `Weekly`
   - Start: Choose a date (e.g., next Monday)
   - Time: `06:00:00`
   - Repeat every: `1` week on: **Monday**
5. **Actions** tab → **New...**:
   - Action: `Start a program`
   - Program/script: `D:\affiliate-content-creator-skill\tools\schedule_crawl.bat`
6. **Conditions** tab:
   - Uncheck **Stop if the computer switches to battery power**
   - Uncheck **Start the task only if computer is on AC power**
7. **Settings** tab:
   - Check **Run task as soon as possible after a scheduled start is missed**
   - Check **If the task fails, restart every 30 minutes** (up to 3 times)
   - Uncheck **Stop the task if it runs longer than**
8. Click **OK** — enter your Windows password when prompted

### Manual Test
```cmd
D:\affiliate-content-creator-skill\tools\schedule_crawl.bat
```
Check `D:\affiliate-content-creator-skill\tools\crawl_log.txt` for results.

---

## Unix / Linux (cron)

1. Make the shell script executable:
```bash
chmod +x /path/to/affiliate-content-creator-skill/tools/schedule_crawl.sh
```

2. Open crontab:
```bash
crontab -e
```

3. Add this line:
```
0 6 * * 1 /path/to/affiliate-content-creator-skill/tools/schedule_crawl.sh
```

4. Verify the cron entry:
```bash
crontab -l
```

### Manual Test
```bash
bash /path/to/affiliate-content-creator-skill/tools/schedule_crawl.sh
```
Check `crawl_log.txt` in the `tools/` directory.

---

## macOS (launchd)

Create a plist file at `~/Library/LaunchAgents/com.affiliate-content-creator.knowledge-updater.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.affiliate-content-creator.knowledge-updater</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/affiliate-content-creator-skill/tools/schedule_crawl.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>6</integer>
        <key>Minute</key>
        <integer>0</integer>
        <key>Weekday</key>
        <integer>1</integer>
    </dict>
    <key>RunAtLoad</key>
    <false/>
    <key>StandardOutPath</key>
    <string>/path/to/affiliate-content-creator-skill/tools/crawl_log.txt</string>
    <key>StandardErrorPath</key>
    <string>/path/to/affiliate-content-creator-skill/tools/crawl_log.txt</string>
</dict>
</plist>
```

Then load it:
```bash
launchctl load ~/Library/LaunchAgents/com.affiliate-content-creator.knowledge-updater.plist
```

---

## Logging & Monitoring

After each crawl run, check:
1. `tools/crawl_log.txt` — run log with timestamps and entry counts
2. `SECOND-KNOWLEDGE-BRAIN.md` → Section 11 → check new entries appended
3. `.url_cache.json` — verify the URL hash cache is growing

### Health Check
If no new entries appear for 3 consecutive weeks, the crawler's HTML parser may have broken due to search result format changes. In that case, update `extract_results_from_search_html()` in `knowledge_updater.py` to match the new format.

---

## First Crawl — Quick Start

To run the first crawl immediately (no need to wait for Monday):
```bash
python tools/knowledge_updater.py
# or
python tools/knowledge_updater.py --dry-run   # preview without writing
```

Verify ≥ 10 entries were added to `SECOND-KNOWLEDGE-BRAIN.md` Section 11.
