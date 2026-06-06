<p align="center">
  <img src="https://img.shields.io/badge/status-production%20ready-22c55e?style=for-the-badge" alt="Status: Production Ready"/>
  <img src="https://img.shields.io/badge/license-MIT-3b82f6?style=for-the-badge" alt="License: MIT"/>
  <img src="https://img.shields.io/badge/ai-agent%20skill-8b5cf6?style=for-the-badge" alt="AI Agent Skill"/>
</p>

<p align="center">
  <h1 align="center">🤖 affiliate-content-creator</h1>
  <p align="center"><em>Autonomous affiliate product discovery, video content creation, and cross-platform posting for TikTok & Facebook</em></p>
</p>

---

> **What this is**: An AI agent skill that discovers trending affiliate products, profiles the target audience, generates optimized short-form video scripts with A/B hooks, enforces compliance gates, and auto-posts content to TikTok and Facebook — all from a single command.

---

## 📋 Table of Contents

- [How It Works](#-how-it-works)
- [Quick Start](#-quick-start)
- [The 6-Stage Harness](#-the-6-stage-harness)
- [Sub-Skills](#-sub-skills)
- [Cross-Skill Dependencies](#-cross-skill-dependencies)
- [Quality Gates](#-quality-gates)
- [Knowledge Pipeline](#-knowledge-pipeline)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Testing](#-testing)
- [Architecture & Design Decisions](#-architecture--design-decisions)
- [License](#-license)

---

## ⚡ How It Works

```
User: "/affiliate-content-creator skincare"

                                    ┌──────────────────────┐
                                    │   User Input         │
                                    │  (niche or URL)      │
                                    └─────────┬────────────┘
                                              │
          ┌───────────────────────────────────▼───────────────────────────────────┐
          │                                                                       │
          │   Stage 1 ──► Platform Scan ──► Top 5 products, commission-weighted   │
          │   Stage 2 ──► Audience Targeting ──► Persona card (pain + motivators)│
          │   Stage 3 ──► Content Drafter ──► Script + caption + hashtags         │
          │   Stage 4 ──► A/B Hooks ──► 5 variants, 5 psychological triggers     │
          │   Stage 5 ──► Quality Gate ──► 8 compliance checks + evidence verify  │
          │   Stage 6 ──► Auto-Post ──► TikTok/Facebook or manual-post fallback  │
          │                                                                       │
          └───────────────────────────────────────────────────────────────────────┘
                                              │
                                              ▼
                              ┌──────────────────────────┐
                              │   Content Package         │
                              │   + posts-log.json        │
                              └──────────────────────────┘
```

### What the user gets back

A complete **Content Package** containing:
- **Product**: Name, category, commission rate, trending score, affiliate URL
- **Audience Persona**: Demographics, pain points, purchase motivators
- **Video Script**: Full 30–60s script with HOOK → PROBLEM → DEMO → PROOF → CTA → DISCLOSURE
- **Caption + Hashtags**: Ready to copy-paste
- **A/B Hook Variants**: 5 alternatives with distinct psychological triggers
- **Quality Report**: PASS with evidence verification
- **Post URLs**: TikTok and/or Facebook links (or manual-post package if APIs unavailable)

---

## 🚀 Quick Start

```bash
# Basic — agent picks the best trending niche automatically
/affiliate-content-creator

# Targeted — specify a niche
/affiliate-content-creator skincare

# Direct product URL — skip discovery, go straight to content
/affiliate-content-creator https://shopee.vn/product/12345?af=ABCDEF

# Localized — target a specific market
/affiliate-content-creator làm đẹp Vietnam Shopee
```

### Prerequisites

- An AI agent runtime that supports the `Skill()` invocation pattern (Claude Code, or compatible)
- Optional: TikTok Developer App + Meta Business Manager credentials for auto-posting

---

## 🔧 The 6-Stage Harness

Each stage is an independent sub-skill invoked by the main harness. Every stage has a quality gate with a recovery procedure if it fails.

| Stage | Sub-Skill | What It Does | Quality Gate | Recovery |
|-------|-----------|-------------|--------------|----------|
| **1** | `sub-platform-scanner` | Scans TikTok Shop, Facebook, Shopee, Lazada for trending products | ≥ 3 products, ≥ 1 with commission ≥ 5% | Broaden niche × 2, then ask user |
| **2** | `sub-audience-targeting` | Builds full persona card (demographics + psychographics) | ≥ 3 pain points + ≥ 2 motivators | Fallback to knowledge base |
| **3** | `sub-content-drafter` | Writes script, caption, hashtags, on-screen overlays | 150–300 words, disclosure, single CTA | 1 retry with fix instructions |
| **4** | `sub-ab-title-generator` | Generates 3–5 hook variants using 5 trigger types | ≥ 3 variants, distinct triggers, ≤ 70% similarity | 1 retry |
| **5** | `sub-quality-reviewer` | Runs 8 compliance checks + evidence claims verification | ALL 8 checks PASS | 2 fix-and-retry cycles |
| **6** | `sub-platform-poster` | Posts to TikTok & Facebook; logs to posts-log.json | Log written, post URL or manual-post saved | 3 attempts → manual-post fallback |

### Retry & Recovery Summary

```
Stage 1:  < 3 products? → Broaden niche → retry (max 2) → ask user for URL
Stage 5:  FAIL? → fix → retry (max 2) → present to user
Stage 6:  API down? → retry with backoff (3) → manual-post package
          No credentials? → immediate manual-post package
```

---

## 📦 Sub-Skills

| Sub-Skill | File | Stage |
|-----------|------|-------|
| Platform Scanner | [`skills/sub-platform-scanner.md`](skills/sub-platform-scanner.md) | 1 |
| Audience Targeting | [`skills/sub-audience-targeting.md`](skills/sub-audience-targeting.md) | 2 |
| Content Drafter | [`skills/sub-content-drafter.md`](skills/sub-content-drafter.md) | 3 |
| A/B Title Generator | [`skills/sub-ab-title-generator.md`](skills/sub-ab-title-generator.md) | 4 |
| Quality Reviewer | [`skills/sub-quality-reviewer.md`](skills/sub-quality-reviewer.md) | 5 |
| Platform Poster | [`skills/sub-platform-poster.md`](skills/sub-platform-poster.md) | 6 |

---

## 🔗 Cross-Skill Dependencies

This skill integrates with the **research-first-reasoning** meta-skill (Skill 7) for evidence-based claims verification.

```
sub-quality-reviewer → Skill("research-first-reasoning") → evidence citations
```

At Stage 5, every factual claim in the script is checked against credible sources. Claims flagged as `UNSUBSTANTIATED`, `EXAGGERATED`, or `MISLEADING` automatically fail the quality gate and must be rewritten.

---

## ✅ Quality Gates

Before any content is posted, all 10 checks must pass:

| # | Check | Why It Matters |
|---|-------|---------------|
| 1 | Affiliate link is active (HTTP 200) | Broken links = lost commissions |
| 2 | Commission rate ≥ 5% | Revenue optimisation |
| 3 | Persona has ≥ 3 pain points + ≥ 2 motivators | Audience-first approach |
| 4 | Script 150–300 words (30–60s) | Platform algorithm optimisation |
| 5 | Affiliate disclosure in script + caption | FTC compliance, account safety |
| 6 | Single clear CTA | Conversion optimisation |
| 7 | Hook scores ≥ 7/10 | Engagement threshold |
| 8 | ≥ 3 A/B hook variants, distinct triggers | Split-test readiness |
| 9 | No prohibited claims | Legal compliance |
| 10 | Platform policy compliance (TikTok + Meta) | Account suspension prevention |

---

## 🧠 Knowledge Pipeline

The skill self-improves weekly through an automated knowledge crawler.

```
┌─────────────────────────────────────────────────────────┐
│                   tools/knowledge_updater.py              │
│                                                         │
│  TikTok Newsroom ─┐                                     │
│  Meta Business ───┤  Crawl → Deduplicate → Append to    │
│  Reddit ──────────┤  (SHA-256)    SECOND-KNOWLEDGE-     │
│  ArXiv ───────────┘               BRAIN.md              │
│                                                         │
│  Schedule: Monday 06:00 via cron / Task Scheduler       │
└─────────────────────────────────────────────────────────┘
```

**Schedule**: Weekly, Monday 06:00
- [Windows: Task Scheduler](docs/schedule-setup.md#windows-task-scheduler)
- [Linux: cron](docs/schedule-setup.md#unix--linux-cron)
- [macOS: launchd](docs/schedule-setup.md#macos-launchd)

---

## 📁 Project Structure

```
affiliate-content-creator-skill/
├── CLAUDE.md                       # Skill identity & configuration
├── README.md                       # This file
├── PROJECT-detail.md               # Full technical specification
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md  # Build roadmap (all phases ✓)
├── SECOND-KNOWLEDGE-BRAIN.md       # Self-improving domain knowledge base
├── idea.txt                        # Original concept prompt
├── posts-log.json                  # Post execution log
├── posts-log.schema.json           # JSON Schema for posts log
│
├── skills/                         # 📚 All skill definition files
│   ├── main.md                     # Main orchestration harness
│   ├── sub-platform-scanner.md     # Stage 1 — Product discovery
│   ├── sub-audience-targeting.md   # Stage 2 — Audience persona
│   ├── sub-content-drafter.md      # Stage 3 — Script writing
│   ├── sub-ab-title-generator.md   # Stage 4 — A/B hooks
│   ├── sub-quality-reviewer.md     # Stage 5 — Compliance + evidence
│   └── sub-platform-poster.md      # Stage 6 — Auto-posting
│
├── tests/
│   └── test-scenarios.md           # 7 test scenarios with pass/fail criteria
│
├── tools/                          # 🛠 Supporting automation tools
│   ├── knowledge_updater.py        # Knowledge crawl pipeline
│   ├── schedule_crawl.bat          # Windows Task Scheduler wrapper
│   └── schedule_crawl.sh           # Unix cron wrapper
│
└── docs/                           # 📖 Documentation
    ├── api-authentication.md       # TikTok + Meta OAuth setup guide
    └── schedule-setup.md           # Cross-platform scheduling guide
```

---

## ⚙️ Configuration

### Environment Variables (for auto-posting)

| Variable | Required For | Description |
|----------|-------------|-------------|
| `TIKTOK_CLIENT_KEY` | TikTok posting | TikTok Developer App client key |
| `TIKTOK_CLIENT_SECRET` | TikTok posting | TikTok Developer App client secret |
| `TIKTOK_ACCESS_TOKEN` | TikTok posting | OAuth 2.0 access token |
| `TIKTOK_REFRESH_TOKEN` | TikTok posting | OAuth 2.0 refresh token |
| `TIKTOK_OPEN_ID` | TikTok posting | TikTok user open ID |
| `META_APP_ID` | Facebook posting | Meta App ID |
| `META_APP_SECRET` | Facebook posting | Meta App secret |
| `META_PAGE_ID` | Facebook posting | Facebook Business Page ID |
| `META_ACCESS_TOKEN` | Facebook posting | Long-lived page access token |

> **No credentials? No problem.** The skill automatically falls back to manual-post mode at Stage 6 — you still get the full content package.

See [`docs/api-authentication.md`](docs/api-authentication.md) for the complete OAuth setup guide.

---

## 🧪 Testing

Seven test scenarios covering the full surface area:

| # | Scenario | What It Tests |
|---|----------|--------------|
| 1 | Basic niche ("skincare") | Full golden path through all 6 stages |
| 2 | Product URL supplied directly | Stage 1 skip, URL extraction |
| 3 | API unavailable | Graceful degradation to manual-post |
| 4 | Quality gate failure → fix → retry | Self-correction loop (max 2 cycles) |
| 5 | No products found → broaden → retry | Niche broadening + user prompt |
| 6 | A/B hooks — all 5 triggers | Hook variant diversity + scoring |
| 7 | Vietnamese market + Shopee | Localization, timezone, local hashtags |

See [`tests/test-scenarios.md`](tests/test-scenarios.md) for full details.

---

## 🏗 Architecture & Design Decisions

1. **Auto-discovery by default** — if no niche supplied, agent picks the highest-opportunity trending niche
2. **Audience-first scripting** — persona card built before any writing, preventing generic "feature dump" scripts
3. **A/B hooks are mandatory** — always ≥ 3 variants with distinct psychological triggers
4. **Compliance gate before posting** — FTC + platform policy checks prevent account suspension
5. **Graceful degradation everywhere** — no single API failure crashes the harness
6. **Commission-weighted product selection** — `trending_score × commission_rate`, optimising for revenue
7. **Evidence-based claims verification** — via cross-skill integration with research-first-reasoning

---

## 📄 License

MIT — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <sub>Built with ❤️ for affiliate marketers who value their time.</sub>
</p>
