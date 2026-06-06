"""
knowledge_updater.py — Skill 2: affiliate-content-creator
Crawls affiliate marketing news, TikTok/Facebook algorithm updates, trending product data,
and relevant research papers, then appends new entries to SECOND-KNOWLEDGE-BRAIN.md.

Schedule: Weekly, Monday 06:00 local time
Usage: python knowledge_updater.py [--topic <keyword>] [--dry-run]
"""

import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import argparse
    import urllib.request
    import urllib.parse
except ImportError as e:
    print(f"[ERROR] Missing stdlib module: {e}")
    sys.exit(1)

BRAIN_PATH = Path(__file__).parent.parent / "SECOND-KNOWLEDGE-BRAIN.md"
CACHE_PATH = Path(__file__).parent / ".url_cache.json"
MIN_ENTRIES_PER_RUN = 5
TODAY = datetime.now().strftime("%Y-%m-%d")

SOURCES = [
    {
        "name": "TikTok Newsroom",
        "search_query": "TikTok affiliate marketing platform updates 2025",
        "type": "news",
        "priority": 1,
    },
    {
        "name": "Meta Business Blog",
        "search_query": "Facebook Instagram affiliate marketing Reels algorithm 2025",
        "type": "news",
        "priority": 1,
    },
    {
        "name": "Reddit r/affiliatemarketing",
        "search_query": "site:reddit.com/r/affiliatemarketing TikTok Shop best practices 2025",
        "type": "forum",
        "priority": 2,
    },
    {
        "name": "ArXiv cs.IR — Recommender Systems",
        "search_query": "arxiv.org cs.IR click-through rate prediction short video recommendation 2025",
        "type": "paper",
        "priority": 1,
    },
    {
        "name": "ArXiv cs.LG — Content Ranking",
        "search_query": "arxiv.org machine learning social media content ranking affiliate 2025",
        "type": "paper",
        "priority": 2,
    },
    {
        "name": "Google Trends — Affiliate Categories",
        "search_query": "trending product categories affiliate marketing TikTok Shop 2025",
        "type": "trends",
        "priority": 2,
    },
    {
        "name": "Affiliate Marketing News",
        "search_query": "affiliate marketing news TikTok Facebook commissions changes 2025",
        "type": "news",
        "priority": 1,
    },
    {
        "name": "Hook & Copywriting Research",
        "search_query": "viral TikTok hook formulas conversion rate optimization short-form video 2025",
        "type": "practice",
        "priority": 2,
    },
]


def load_url_cache() -> set:
    """Load the set of already-processed URLs from the local cache file."""
    if not CACHE_PATH.exists():
        return set()
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return set(data.get("processed_hashes", []))
    except (json.JSONDecodeError, KeyError):
        return set()


def save_url_cache(processed_hashes: set) -> None:
    """Persist the updated set of processed URL hashes."""
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump({"processed_hashes": list(processed_hashes), "last_updated": TODAY}, f, indent=2)


def url_to_hash(url: str) -> str:
    """Return the SHA-256 hash of a URL string for deduplication."""
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def build_search_url(query: str) -> str:
    """Build a URL-encoded search query string for a web search API."""
    encoded = urllib.parse.quote_plus(query)
    return f"https://api.search.brave.com/res/v1/web/search?q={encoded}&count=5"


def fetch_url(url: str, timeout: int = 10) -> Optional[str]:
    """Fetch the content of a URL. Returns None on error."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; KnowledgeUpdater/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"[WARN] Failed to fetch {url}: {e}")
        return None


def extract_results_from_search_html(html: str, source_name: str) -> list[dict]:
    """
    Parse search results from raw HTML.
    Returns a list of dicts: {title, url, snippet}.
    This is a best-effort heuristic parser — production use should use a proper search API.
    """
    results = []
    title_pattern = re.compile(r'<h[23][^>]*>(.*?)</h[23]>', re.DOTALL | re.IGNORECASE)
    url_pattern = re.compile(r'href="(https?://[^"]+)"', re.IGNORECASE)
    snippet_pattern = re.compile(r'<p[^>]*>(.*?)</p>', re.DOTALL | re.IGNORECASE)

    titles = [re.sub(r'<[^>]+>', '', t).strip() for t in title_pattern.findall(html)]
    urls = [u for u in url_pattern.findall(html) if "google" not in u and "bing" not in u]
    snippets = [re.sub(r'<[^>]+>', '', s).strip() for s in snippet_pattern.findall(html)]

    for i, (title, url) in enumerate(zip(titles[:5], urls[:5])):
        snippet = snippets[i] if i < len(snippets) else ""
        if title and url and len(title) > 10:
            results.append({
                "title": title[:200],
                "url": url[:500],
                "snippet": snippet[:300],
                "source": source_name,
            })
    return results


def score_relevance(result: dict, topic_override: Optional[str] = None) -> float:
    """
    Score a result for relevance to affiliate content creation.
    Higher = more relevant. Range: 0.0 to 1.0.
    """
    keywords = [
        "affiliate", "tiktok", "facebook", "commission", "hook", "conversion",
        "trending", "short-form", "reels", "video", "creator", "e-commerce",
        "recommendation", "ctr", "shopee", "lazada"
    ]
    if topic_override:
        keywords.extend(topic_override.lower().split())

    text = (result.get("title", "") + " " + result.get("snippet", "")).lower()
    matches = sum(1 for kw in keywords if kw in text)
    return min(matches / max(len(keywords) * 0.5, 1), 1.0)


def format_brain_entry(result: dict) -> str:
    """Format a search result as a SECOND-KNOWLEDGE-BRAIN.md table row."""
    title = result.get("title", "Unknown Title")
    source = result.get("source", "Unknown")
    url = result.get("url", "")
    snippet = result.get("snippet", "")[:200].replace("|", "/").replace("\n", " ")
    return f"| {title[:80]} | {source} | {TODAY} | {url[:100]} | {snippet} |"


def append_to_brain(entries: list[str], dry_run: bool = False) -> int:
    """
    Append new entries to the Knowledge Update Log table in SECOND-KNOWLEDGE-BRAIN.md.
    Returns the count of entries appended.
    """
    if not entries:
        print("[INFO] No new entries to append.")
        return 0

    if dry_run:
        print(f"[DRY RUN] Would append {len(entries)} entries:")
        for entry in entries:
            print(f"  {entry}")
        return len(entries)

    if not BRAIN_PATH.exists():
        print(f"[ERROR] SECOND-KNOWLEDGE-BRAIN.md not found at {BRAIN_PATH}")
        return 0

    with open(BRAIN_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Append entries to the Knowledge Update Log section
    log_header = "## 11. Knowledge Update Log"
    if log_header not in content:
        content += f"\n\n{log_header}\n\n| Date | Source | Entries Added | Notes |\n|------|--------|--------------|-------|\n"

    insert_block = "\n".join(entries)
    content += f"\n{insert_block}\n"

    with open(BRAIN_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[INFO] Appended {len(entries)} new entries to SECOND-KNOWLEDGE-BRAIN.md")
    return len(entries)


def run(topic_override: Optional[str] = None, dry_run: bool = False) -> None:
    """Main crawl pipeline entry point."""
    print(f"[START] knowledge_updater.py — {TODAY}")
    print(f"[CONFIG] Topic override: {topic_override or 'None'}")
    print(f"[CONFIG] Dry run: {dry_run}")

    processed_hashes = load_url_cache()
    new_entries: list[str] = []
    new_hashes: set = set()

    sources_to_run = sorted(SOURCES, key=lambda s: s["priority"])

    for source in sources_to_run:
        query = source["search_query"]
        if topic_override:
            query = f"{topic_override} {query}"

        print(f"\n[SCAN] {source['name']} — query: {query[:80]}...")
        search_url = build_search_url(query)
        html = fetch_url(search_url)

        if not html:
            print(f"[SKIP] No response from search for: {source['name']}")
            continue

        results = extract_results_from_search_html(html, source["name"])
        print(f"[FOUND] {len(results)} raw results")

        for result in results:
            url_hash = url_to_hash(result["url"])

            if url_hash in processed_hashes or url_hash in new_hashes:
                print(f"[SKIP] Duplicate: {result['url'][:80]}")
                continue

            score = score_relevance(result, topic_override)
            if score < 0.2:
                print(f"[SKIP] Low relevance ({score:.2f}): {result['title'][:60]}")
                continue

            entry = format_brain_entry(result)
            new_entries.append(entry)
            new_hashes.add(url_hash)
            print(f"[ADD] Score {score:.2f}: {result['title'][:60]}")

        if len(new_entries) >= MIN_ENTRIES_PER_RUN * 3:
            print(f"[INFO] Collected enough entries ({len(new_entries)}), stopping early")
            break

    if len(new_entries) < MIN_ENTRIES_PER_RUN:
        print(f"[WARN] Only {len(new_entries)} entries collected (minimum: {MIN_ENTRIES_PER_RUN})")
        print("[WARN] Consider expanding search queries or checking network access")

    # Append update log entry
    if new_entries:
        log_row = f"| {TODAY} | Auto-crawl | {len(new_entries)} | Topic: {topic_override or 'general affiliate marketing'} |"
        new_entries.append(log_row)

    appended = append_to_brain(new_entries, dry_run=dry_run)

    if not dry_run:
        processed_hashes.update(new_hashes)
        save_url_cache(processed_hashes)

    print(f"\n[DONE] Appended {appended} entries. Cache size: {len(processed_hashes) + len(new_hashes)} URLs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update SECOND-KNOWLEDGE-BRAIN.md with fresh affiliate marketing data"
    )
    parser.add_argument(
        "--topic",
        type=str,
        default=None,
        help="Optional topic override to focus the crawl (e.g., 'skincare TikTok')"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Print what would be appended without writing to the file"
    )
    args = parser.parse_args()
    run(topic_override=args.topic, dry_run=args.dry_run)
