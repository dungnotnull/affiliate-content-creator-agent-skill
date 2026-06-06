# PROJECT-detail.md — Skill 2: affiliate-content-creator

## Executive Summary

`affiliate-content-creator` is a fully autonomous harness that discovers trending affiliate products on TikTok Shop and Facebook e-commerce platforms, profiles the ideal audience, generates optimized short-form video scripts with A/B hook variants, enforces quality and compliance gates, then auto-posts finished content to TikTok and Facebook. The agent requires only an optional niche keyword as input; all subsequent steps are self-directed.

---

## Problem Statement

Affiliate content creation on short-form video platforms (TikTok, Facebook Reels) is one of the highest-ROI digital marketing channels in Southeast Asia and globally. However, the workflow is labour-intensive:

1. **Product Discovery** — manually browsing TikTok Shop, Facebook, Shopee, Lazada affiliate dashboards to identify trending items with high commission rates
2. **Audience Research** — understanding who buys the product, what pain points drive purchase, what format resonates
3. **Script Production** — writing hooks, problem framing, product demonstration narration, social proof references, and CTAs
4. **Split-Test Preparation** — generating multiple hook variations to test engagement
5. **Compliance** — checking FTC/ASA affiliate disclosure requirements and platform-specific ad policies
6. **Publishing** — manually uploading videos with captions, hashtags, links, and scheduling

This skill collapses all six steps into a single harness invocation, reducing the human time investment from 4–6 hours per post to under 10 minutes of review.

---

## Target Users & Use Cases

| User Type | Trigger Example | Expected Output |
|-----------|----------------|-----------------|
| Solo affiliate marketer | "Find me a trending product in skincare" | Full TikTok video script + caption + hashtags + posted link |
| Agency content team | "Create 3 videos for fitness gear this week" | 3 complete video packages, each with A/B hooks, scheduled for optimal posting times |
| Beginner creator | Just runs `/affiliate-content-creator` | Agent autonomously picks a trending product and delivers a ready-to-film script |
| Advanced marketer | Supplies a product URL | Agent skips discovery, goes straight to audience profiling and script generation |

---

## Harness Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  affiliate-content-creator                   │
│                       (main.md)                              │
└──────────────────────────┬──────────────────────────────────┘
                           │
          ┌────────────────▼─────────────────┐
          │   Stage 1: Platform Scan          │
          │   sub-platform-scanner.md         │
          │   Input: niche (optional)         │
          │   Output: top-5 candidate products│
          └────────────────┬─────────────────┘
                           │
          ┌────────────────▼─────────────────┐
          │   Stage 2: Audience Targeting     │
          │   sub-audience-targeting.md       │
          │   Input: selected product         │
          │   Output: audience persona card   │
          └────────────────┬─────────────────┘
                           │
          ┌────────────────▼─────────────────┐
          │   Stage 3: Content Strategy +     │
          │   Full Script Draft               │
          │   sub-content-drafter.md          │
          │   Input: product + persona card   │
          │   Output: video script draft      │
          └────────────────┬─────────────────┘
                           │
          ┌────────────────▼─────────────────┐
          │   Stage 4: A/B Hook Variations    │
          │   sub-ab-title-generator.md       │
          │   Input: script draft             │
          │   Output: 3–5 hook alternatives   │
          └────────────────┬─────────────────┘
                           │
          ┌────────────────▼─────────────────┐
          │   Stage 5: Quality Gate Review    │
          │   sub-quality-reviewer.md         │
          │   Input: full package             │
          │   Output: PASS / FAIL + fixes     │
          └────────────────┬─────────────────┘
                           │
          ┌────────────────▼─────────────────┐
          │   Stage 6: Auto-Post              │
          │   sub-platform-poster.md          │
          │   Input: approved package         │
          │   Output: post URL + schedule log │
          └──────────────────────────────────┘
```

---

## Full Sub-Skill Catalog

### sub-platform-scanner.md
- **Purpose**: Discover trending affiliate products on TikTok Shop, Facebook, Shopee, Lazada
- **Inputs**: Optional niche keyword; platform preference (default: both TikTok + Facebook)
- **Outputs**: Ranked list of top-5 products with: name, estimated commission %, trending score, affiliate link
- **Tools**: WebSearch, WebFetch
- **Quality Gate**: At least 3 products found; commission ≥ 5%; trending in last 7 days

### sub-audience-targeting.md
- **Purpose**: Build a full audience persona for the selected product
- **Inputs**: Product name, category, platform
- **Outputs**: Persona card — demographics (age, gender, location), psychographics (pain points, desires, objections), preferred content format, best posting time
- **Tools**: WebSearch (social listening), WebFetch (platform insights pages)
- **Quality Gate**: Persona includes at least 3 pain points and 2 purchase motivators

### sub-content-drafter.md
- **Purpose**: Write the complete short-form video script and caption
- **Inputs**: Product details + audience persona card
- **Outputs**: Full video script (hook → problem → demo → proof → CTA), on-screen text overlays, caption, hashtag set
- **Tools**: WebSearch (competitor content research), Write
- **Quality Gate**: Script ≤ 60 seconds when read aloud; includes affiliate disclosure; has measurable CTA

### sub-ab-title-generator.md
- **Purpose**: Generate 3–5 alternative hooks and titles for A/B testing
- **Inputs**: Primary script hook + product name + audience persona
- **Outputs**: 3–5 hook variants with predicted engagement rationale
- **Tools**: WebSearch (viral hook patterns), Write
- **Quality Gate**: Each variant uses a different psychological trigger (curiosity, fear, aspiration, social proof, shock)

### sub-quality-reviewer.md
- **Purpose**: Enforce compliance, policy adherence, and content quality before posting
- **Inputs**: Complete content package (script + caption + hooks + hashtags)
- **Outputs**: PASS or FAIL report with specific line-level fixes for any failures
- **Tools**: WebSearch (FTC guidelines, TikTok ad policies, Meta commerce policies), Read
- **Quality Gate**: All 8 compliance checks pass; hook effectiveness score ≥ 7/10; CTA is clear and single-action

---

## Skill File Format Specification

### Frontmatter Schema (main.md)
```yaml
---
name: affiliate-content-creator
description: Autonomous affiliate product discovery, video content creation, and platform posting for TikTok & Facebook
---
```

### Required Sections in main.md
1. `## Role & Persona` — expert affiliate marketing strategist + platform algorithm specialist
2. `## Workflow (Harness Flow)` — 6-stage numbered flow with sub-skill invocations
3. `## Sub-skills Available` — list of all sub-skill files
4. `## Tools` — WebSearch, WebFetch, Bash, Read, Write, Skill
5. `## Output Format` — exact structure of the final deliverable package
6. `## Quality Gates` — checklist that must pass before Stage 6 (auto-post)

---

## E2E Execution Flow

```
1. User invokes: /affiliate-content-creator [optional: "skincare"]
2. Main harness reads SECOND-KNOWLEDGE-BRAIN.md for domain context
3. [Stage 1] Invoke sub-platform-scanner → get top-5 products
   3a. If < 3 products found → retry with broader niche → if still < 3, ask user
   3b. Select product with highest (trending_score × commission_rate)
4. [Stage 2] Invoke sub-audience-targeting → get persona card
   4a. If WebSearch unavailable → use SECOND-KNOWLEDGE-BRAIN.md audience data
5. [Stage 3] Invoke sub-content-drafter → draft script + caption + hashtags
   5a. Script must be 30–60 seconds when read aloud (150–300 words)
6. [Stage 4] Invoke sub-ab-title-generator → get 3–5 hook variants
7. [Stage 5] Invoke sub-quality-reviewer → get PASS/FAIL
   7a. If FAIL → fix flagged items → re-run quality gate → max 2 retry cycles
   7b. If still FAIL after 2 cycles → present to user for manual review
8. [Stage 6] Invoke sub-platform-poster → publish to TikTok and/or Facebook
   8a. Log post URL, post time, platform, and selected hook variant
   8b. Save record to posts-log.json in the skill output folder
9. Present final summary to user: product chosen, hook used, post URLs, next steps
```

---

## SECOND-KNOWLEDGE-BRAIN Integration

- **Affiliate Marketing** — TikTok Shop affiliate documentation, Meta Business affiliate program docs
- **Hook Formulas** — Viral short-form hook patterns (curiosity gap, pain-agitate-solve, before/after)
- **Platform Algorithms** — TikTok For You Page factors, Facebook Reels distribution signals
- **Crawl Config**: `tools/knowledge_updater.py` — weekly run, sources: TikTok Newsroom, Meta Business Blog, affiliate marketing forums, ArXiv (recommender systems)
- **Append Format**: `| Title | Source | Date | URL | Key Finding |`

---

## Supporting Tools Spec

### tools/knowledge_updater.py
- **Inputs**: None (scheduled run) or `--topic <keyword>` override
- **Outputs**: Appends new entries to `SECOND-KNOWLEDGE-BRAIN.md`
- **Schedule**: Weekly cron (Monday 06:00)
- **Sources**:
  - TikTok Newsroom (newsroom.tiktok.com)
  - Meta Business Blog (business.facebook.com/blog)
  - Affiliate marketing subreddits via Reddit API
  - ArXiv cs.IR, cs.LG (recommender systems, click-through rate prediction)
  - Google Trends API (trending product categories)
- **Deduplication**: SHA-256 hash of URL, skip if already in brain

---

## Quality Gates

Before Stage 6 (auto-post), ALL of the following must be true:

| # | Gate | Pass Condition |
|---|------|---------------|
| 1 | Product validity | Affiliate link is active; commission ≥ 5% |
| 2 | Audience profile | Persona card has ≥ 3 pain points + ≥ 2 purchase motivators |
| 3 | Script length | 150–300 words (30–60 seconds read aloud) |
| 4 | Affiliate disclosure | Script/caption includes "#ad" or "Affiliate link" disclosure |
| 5 | CTA clarity | Single clear call-to-action (click link, comment keyword, visit store) |
| 6 | Hook strength | Hook scores ≥ 7/10 on curiosity/emotion/relevance scale |
| 7 | A/B variants | ≥ 3 hook variants generated with distinct psychological triggers |
| 8 | Platform policy | No prohibited claims (medical, financial, guaranteed income) |

---

## Test Scenarios

See `tests/test-scenarios.md` for 5+ concrete scenario-based tests.

---

## Key Design Decisions

1. **Auto-discovery by default**: If no niche is supplied, the agent picks the highest-opportunity niche from trending data — this removes the blank-page problem for beginners.
2. **Audience-first scripting**: Persona card is built before any writing begins, preventing generic "product feature dump" scripts that convert poorly.
3. **A/B hooks are mandatory**: The harness always generates ≥ 3 hook variants before quality review — this enforces split-testing discipline even for users who wouldn't think to do it.
4. **Compliance gate before posting**: FTC and platform policy checks run before every post — this prevents account suspension and legal liability.
5. **Graceful degradation**: If TikTok/Facebook APIs are unavailable, the harness outputs the full content package as a ready-to-copy script + caption + hashtag set, with a note that manual posting is required.
6. **Posts log**: Every published post is written to `posts-log.json` — this creates a performance feedback loop (user can later add engagement data and the agent can learn which hooks won).
7. **Commission-weighted product selection**: Products are ranked by `trending_score × commission_rate`, not trending score alone — this ensures the agent optimizes for revenue, not just views.
