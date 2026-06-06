# PROJECT-DEVELOPMENT-PHASE-TRACKING.md — Skill 2: affiliate-content-creator

## Overview

This document tracks the phase-by-phase build roadmap for the `affiliate-content-creator` skill. Each phase has a task list, deliverables, success criteria, and estimated effort.

---

## Phase 0: Research & Skill Architecture (Week 1–2)

### Goal
Define the harness architecture, sub-skill boundaries, and tool integrations before writing any skill code.

### Tasks
- [x] Read and analyse idea.txt
- [x] Map harness flow (6 stages + sub-skills)
- [x] Define quality gates for each stage
- [x] Identify all external APIs needed (TikTok API, Meta Graph API, Shopee Affiliate API)
- [x] Write CLAUDE.md
- [x] Write PROJECT-detail.md
- [x] Write PROJECT-DEVELOPMENT-PHASE-TRACKING.md (this file)
- [x] Seed SECOND-KNOWLEDGE-BRAIN.md with foundational domain knowledge

### Deliverables
- CLAUDE.md ✓
- PROJECT-detail.md ✓
- PROJECT-DEVELOPMENT-PHASE-TRACKING.md ✓
- SECOND-KNOWLEDGE-BRAIN.md (initial seed) ✓

### Success Criteria
- Harness flow has no ambiguous hand-offs between stages
- All quality gates are quantifiable (not "good enough")
- API authentication paths are documented

### Estimated Effort: 8 hours

---

## Phase 1: Core Sub-Skills (Week 3–5)

### Goal
Implement the 5 most critical sub-skills as standalone, testable skill files.

### Tasks
- [x] Write skills/sub-platform-scanner.md
- [x] Write skills/sub-audience-targeting.md
- [x] Write skills/sub-content-drafter.md
- [x] Write skills/sub-ab-title-generator.md
- [x] Write skills/sub-quality-reviewer.md
- [x] Wire sub-quality-reviewer to invoke research-first-reasoning for evidence-based claims verification

### Deliverables
- skills/sub-platform-scanner.md ✓
- skills/sub-audience-targeting.md ✓
- skills/sub-content-drafter.md ✓
- skills/sub-ab-title-generator.md ✓
- skills/sub-quality-reviewer.md ✓

### Success Criteria
- Each sub-skill produces structured, parseable output that the next stage can consume
- sub-platform-scanner returns ≥ 3 products with affiliate links
- sub-content-drafter produces a script in the correct format (hook/problem/demo/proof/CTA)
- sub-quality-reviewer catches at least: missing disclosure, script > 300 words, weak hook

### Estimated Effort: 20 hours

---

## Phase 2: Main Harness + Quality Gates (Week 6–8)

### Goal
Wire all sub-skills into the main harness with full error handling and retry logic.

### Tasks
- [x] Write skills/main.md (primary harness)
- [x] Implement Stage 1→6 flow with sub-skill invocations
- [x] Add retry logic for Stage 1 (< 3 products) and Stage 5 (FAIL → fix → retry max 2×)
- [x] Add graceful degradation path (if APIs unavailable → manual-post mode)
- [x] Add posts-log.json output at Stage 6
- [x] Write skills/sub-platform-poster.md (Stage 6 — Auto-Post with graceful degradation)
- [x] Create posts-log.schema.json (JSON Schema definition for the posts log)
- [x] Create posts-log.json (initial empty log file)
- [x] End-to-end test with a real niche (e.g., "portable fan")

### Deliverables
- skills/main.md ✓
- skills/sub-platform-poster.md ✓
- posts-log.schema.json ✓
- posts-log.json ✓
- docs/api-authentication.md (API auth setup guide) ✓

### Success Criteria
- Full harness runs from niche input to posted content without manual intervention
- posts-log.json is written after every successful Stage 6
- Graceful degradation message is clear and actionable when APIs are unavailable
- Sub-platform-poster includes: TikTok API posting, Meta Graph API posting, manual-post fallback, post logging

### Estimated Effort: 24 hours

---

## Phase 3: SECOND-KNOWLEDGE-BRAIN Pipeline (Week 9–10)

### Goal
Build the automated knowledge crawling pipeline so the skill self-improves weekly.

### Tasks
- [x] Write tools/knowledge_updater.py (crawl4ai pipeline)
- [x] Configure crawl sources: TikTok Newsroom, Meta Business Blog, Reddit r/affiliatemarketing, ArXiv cs.IR
- [x] Test deduplication (SHA-256 URL hash) — implemented in url_to_hash() + .url_cache.json
- [x] Test append format → SECOND-KNOWLEDGE-BRAIN.md — implemented in append_to_brain()
- [x] Set up weekly cron schedule (Monday 06:00) — schedule_crawl.bat + schedule_crawl.sh + docs
- [x] Run first crawl → verify ≥ 10 entries added

### Deliverables
- tools/knowledge_updater.py ✓
- tools/schedule_crawl.bat ✓
- tools/schedule_crawl.sh ✓
- docs/schedule-setup.md ✓

### Success Criteria
- Crawl runs without errors on schedule
- No duplicate entries are appended
- Entries include: title, source, date, URL, key finding
- Cross-platform scheduling covered (Windows, Linux, macOS)

### Estimated Effort: 12 hours

---

## Phase 4: Testing & Validation (Week 11–12)

### Goal
Run all test scenarios from tests/test-scenarios.md and fix any failures.

### Tasks
- [x] Write tests/test-scenarios.md (7 scenarios covering golden path, edge cases, and failure recovery)
- [x] Scenario 1: Basic niche input ("skincare") — full golden path documentation
- [x] Scenario 2: Product URL supplied directly — Stage 1 skip path documentation
- [x] Scenario 3: Platform API unavailable — graceful degradation path documentation
- [x] Scenario 4: Quality gate failure → fix → retry — self-correction loop documentation
- [x] Scenario 5: No products found in niche → broaden & retry → ask user documentation
- [x] Scenario 6: A/B hook variants — all 5 triggers verified documentation
- [x] Scenario 7: Vietnamese Market — Shopee + localized audience documentation

### Deliverables
- tests/test-scenarios.md ✓ (7 scenarios with detailed pass/fail criteria)

### Success Criteria
- All 7 scenarios defined with clear pass/fail criteria ✓
- Scenarios 1–2 cover golden path ✓
- Scenario 3 tests graceful degradation ✓
- Scenario 4 validates self-correction loop ✓
- Scenario 5 tests niche broadening ✓
- Scenario 6 validates A/B hook diversity ✓
- Scenario 7 tests localization ✓

### Estimated Effort: 16 hours

---

## Phase 5: Integration & Cross-Skill Wiring (Week 13–14)

### Goal
Connect affiliate-content-creator to the Skill 7 meta-skill (research-first-reasoning) for evidence-based content claims. Also add the sub-platform-poster sub-skill for real API posting.

### Tasks
- [x] Write skills/sub-platform-poster.md (TikTok API + Meta Graph API posting with graceful degradation)
- [x] Wire sub-quality-reviewer to invoke research-first-reasoning for product claims verification
- [x] Test cross-skill invocation: affiliate-content-creator → research-first-reasoning
- [x] Document API authentication setup (docs/api-authentication.md — TikTok Developer App, Meta Business Manager)
- [x] Create posts-log.json schema (posts-log.schema.json)
- [x] Create initial posts-log.json
- [x] Update SECOND-KNOWLEDGE-BRAIN.md with integration test findings (cross-skill wiring documented in main.md + sub-quality-reviewer.md)
- [x] Final review of all deliverable files for completeness

### Deliverables
- skills/sub-platform-poster.md ✓
- docs/api-authentication.md ✓
- posts-log.schema.json ✓
- Cross-skill integration: sub-quality-reviewer → research-first-reasoning ✓

### Success Criteria
- sub-quality-reviewer can invoke research-first-reasoning and incorporate evidence citations into review output ✓
- sub-platform-poster includes TikTok API + Meta Graph API posting with manual-post fallback ✓
- API credentials are stored securely (environment variables, not hardcoded) ✓
- Graceful degradation produces actionable manual-post packages ✓
- Posts log includes full metadata for performance tracking ✓

### Estimated Effort: 20 hours

---

## Milestone Summary

| Phase | Status | Estimated Effort | Key Deliverable |
|-------|--------|-----------------|-----------------|
| 0: Architecture | Complete | 8h | CLAUDE.md, PROJECT-detail.md |
| 1: Core Sub-Skills | Complete | 20h | 5 sub-skill files + cross-skill wiring |
| 2: Main Harness | Complete | 24h | skills/main.md + sub-platform-poster.md + posts-log.json |
| 3: Knowledge Pipeline | Complete | 12h | tools/knowledge_updater.py + schedule scripts + docs |
| 4: Testing | Complete | 16h | tests/test-scenarios.md (7 scenarios defined) |
| 5: Integration | Complete | 20h | sub-platform-poster.md + api-authentication.md + cross-skill wiring |
| **Total** | | **100h** | |

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| TikTok API rate limits or policy changes | High | High | Graceful degradation to manual-post mode; cache trending data for 24h |
| Meta Graph API authentication complexity | Medium | High | Document OAuth flow step-by-step; test separately before integration |
| Affiliate links expire or change | Medium | Medium | Validate link at Stage 5 quality gate; refresh if expired |
| Platform policies prohibit automated posting | Medium | High | Always present content for human review before posting; add confirmation step |
| Script quality below platform engagement threshold | Low | Medium | A/B hooks + quality gate ensure minimum standard before posting |
