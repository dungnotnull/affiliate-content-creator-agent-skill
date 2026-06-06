# CLAUDE.md — Skill: affiliate-content-creator

## Skill Identity

- **Name**: affiliate-content-creator
- **Tagline**: Autonomous affiliate product discovery, video content creation, and platform posting for TikTok & Facebook
- **Current Phase**: Phase 0 — Architecture & Specification Complete
- **Skill File**: `skills/main.md`

---

## Problem This Skill Solves

Affiliate marketers spend hours manually browsing e-commerce platforms (TikTok Shop, Facebook Marketplace, Shopee, Lazada) to find trending products, then more hours scripting video content, designing hooks, writing captions, and manually posting. This skill fully automates that pipeline: the agent discovers trending affiliate products autonomously (or accepts a user-supplied niche), profiles the target audience, builds optimized video scripts with A/B hook variations, applies quality gates, and posts the finished content directly to TikTok and Facebook — all without human intervention beyond the initial trigger.

---

## Harness Flow Summary

```
/affiliate-content-creator [niche?]
  │
  ├── Stage 1: Platform Scan          → sub-platform-scanner.md
  │     Discover trending products on TikTok Shop / Facebook / Shopee / Lazada
  │
  ├── Stage 2: Audience Targeting     → sub-audience-targeting.md
  │     Profile demographic + interest + pain-point for top candidate products
  │
  ├── Stage 3: Content Strategy       → sub-content-drafter.md
  │     Select content format, generate video script, hooks, body, CTA
  │
  ├── Stage 4: A/B Hook Variations    → sub-ab-title-generator.md
  │     Generate 3–5 alternative hooks/titles for split testing
  │
  ├── Stage 5: Quality Gate Review    → sub-quality-reviewer.md
  │     Check FTC compliance, platform policy, hook strength, CTA clarity
  │
  └── Stage 6: Auto-Post              → sub-platform-poster.md
        Schedule + publish to TikTok and/or Facebook with captions & hashtags
```

---

## Sub-Skills

| File                               | Purpose                                                                       |
| ---------------------------------- | ----------------------------------------------------------------------------- |
| `skills/sub-platform-scanner.md`   | Scan TikTok Shop / Facebook / Shopee affiliate programs for trending products |
| `skills/sub-audience-targeting.md` | Build demographic + psychographic + pain-point profile for the product niche  |
| `skills/sub-content-drafter.md`    | Write full video script: hook → problem → demo → proof → CTA                  |
| `skills/sub-ab-title-generator.md` | Generate 3–5 A/B hook & title variants for split testing                      |
| `skills/sub-quality-reviewer.md`   | Enforce FTC compliance, platform policies, hook effectiveness, CTA clarity    |

---

## Tools Required

- `WebSearch` — find trending products, affiliate programs, hashtag trends
- `WebFetch` — fetch product pages, TikTok/Facebook affiliate dashboards
- `Bash` — run auto-posting scripts (TikTok API, Facebook Graph API)
- `Read` / `Write` — persist scripts, strategies, and post records
- `Skill` — invoke sub-skills at each harness stage

---

## Knowledge Sources

- TikTok Shop Affiliate Center trending feed
- Facebook Affiliate / Meta Business Suite
- Shopee Affiliate Program trending items
- Lazada Affiliate trending items
- SECOND-KNOWLEDGE-BRAIN.md — affiliate marketing frameworks, hook formulas, platform algorithms

---

## Supporting Python Tools

| File                         | Purpose                                                                                                                   |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `tools/knowledge_updater.py` | Crawls affiliate marketing news, trending hashtags, and platform algorithm updates → appends to SECOND-KNOWLEDGE-BRAIN.md |

---

## Active Development Tasks — All Complete

- [x] Write CLAUDE.md
- [x] Write PROJECT-detail.md
- [x] Write PROJECT-DEVELOPMENT-PHASE-TRACKING.md
- [x] Write SECOND-KNOWLEDGE-BRAIN.md
- [x] Write skills/main.md (with full retry logic + graceful degradation)
- [x] Write skills/sub-platform-scanner.md
- [x] Write skills/sub-audience-targeting.md
- [x] Write skills/sub-content-drafter.md
- [x] Write skills/sub-ab-title-generator.md
- [x] Write skills/sub-quality-reviewer.md (with research-first-reasoning cross-skill wiring)
- [x] Write skills/sub-platform-poster.md (TikTok + Meta API posting, manual-post fallback)
- [x] Write tools/knowledge_updater.py
- [x] Write tools/schedule_crawl.bat (Windows Task Scheduler wrapper)
- [x] Write tools/schedule_crawl.sh (Unix cron wrapper)
- [x] Write tests/test-scenarios.md (7 scenarios)
- [x] Write docs/api-authentication.md (TikTok + Meta OAuth setup)
- [x] Write docs/schedule-setup.md (cron/Task Scheduler/launchd instructions)
- [x] Write posts-log.schema.json
- [x] Create posts-log.json

---

## References

- `PROJECT-detail.md` — full technical specification
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — build roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` — domain knowledge base
- Root `D:\Dungchan\CLAUDE.md` — master skill library spec
