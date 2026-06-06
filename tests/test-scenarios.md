# test-scenarios.md — Skill 2: affiliate-content-creator

## Overview

This document contains 7 scenario-based tests for the `affiliate-content-creator` skill. Each scenario defines the input conditions, expected behavior at each harness stage, expected output, and the pass/fail criteria.

Tests are designed to cover the golden path, edge cases, and failure recovery paths.

---

## Scenario 1: Basic Niche Input — Full Golden Path

**Description**: User supplies a single niche keyword; the harness completes all 6 stages autonomously.

**Input**:
```
/affiliate-content-creator skincare
```

**Expected Behavior**:
- Stage 1 (Platform Scanner): Returns ≥ 3 skincare products from TikTok Shop or Shopee with commission ≥ 5%. Selects the highest composite-score product.
- Stage 2 (Audience Targeting): Builds a persona card with age range 20–35, ≥ 3 pain points (e.g., acne, dryness, uneven tone), ≥ 2 motivators (clear skin, confidence), optimal posting time.
- Stage 3 (Content Drafter): Produces a 150–300 word script with HOOK/PROBLEM/DEMO/PROOF/CTA/DISCLOSURE sections. Caption with #ad. 5–10 hashtags.
- Stage 4 (A/B Generator): Returns 5 hook variants covering all 5 psychological triggers. Each scores ≥ 6.0/10.
- Stage 5 (Quality Reviewer): All 8 checks pass. Status: PASS.
- Stage 6 (Poster): Posts to TikTok and Facebook; logs to posts-log.json.

**Expected Output**: Complete Content Package delivered; post URL logged.

**Pass Criteria**:
- All 6 stages complete without error
- Content Package matches the required output format
- posts-log.json entry is written
- No prohibited claims in script
- Affiliate disclosure present in both script and caption

**Fail Criteria**:
- Any stage exits with an unhandled error
- Script contains a prohibited claim
- Disclosure is absent
- posts-log.json is not written after Stage 6

---

## Scenario 2: Product URL Supplied Directly

**Description**: User skips product discovery by supplying a direct product URL with an affiliate link. Harness should skip Stage 1 and start at Stage 2.

**Input**:
```
/affiliate-content-creator https://shopee.vn/product/12345?af=ABCDEF
```

**Expected Behavior**:
- Stage 1 (Platform Scanner): Skipped. Agent fetches product details from the supplied URL instead.
- Stage 2 onward: Full normal flow.

**Expected Output**: Complete Content Package using the supplied product.

**Pass Criteria**:
- Stage 1 is skipped cleanly (no "no products found" error)
- Product details are correctly extracted from the URL
- All downstream stages receive the correct product context

**Fail Criteria**:
- Stage 1 attempts to scan for trending products despite URL being supplied
- Product details are not extracted from the URL

---

## Scenario 3: Platform API Unavailable — Graceful Degradation

**Description**: TikTok and Facebook posting APIs return errors at Stage 6. The harness should fall back to a manual-post package.

**Input**:
```
/affiliate-content-creator electronics
```
*Simulated condition: Stage 6 API calls return HTTP 503*

**Expected Behavior**:
- Stages 1–5: Complete normally
- Stage 6: Detects API unavailability. Outputs a complete manual-post package instead of posting. Writes package to a dated file. Displays clear guidance to the user.

**Expected Output**:
```
[MANUAL POST REQUIRED]
Platform API unavailable. Your content package is ready to post manually.
File saved: output/2026-06-05_electronics_content_package.md

Instructions:
1. Copy the script above
2. Record your video
3. Post to TikTok: [paste caption + hashtags]
4. Post to Facebook: [paste caption + hashtags]
5. Affiliate link: [url]
```

**Pass Criteria**:
- No unhandled exception at Stage 6
- Manual-post package file is written with the correct content
- User sees actionable instructions

**Fail Criteria**:
- Harness crashes at Stage 6
- User sees only an error message with no actionable output
- Content package is not saved

---

## Scenario 4: Quality Gate Failure and Self-Correction

**Description**: The first script draft fails the quality gate (missing disclosure + hook score below 7.0). The harness should apply fixes and retry.

**Input**:
```
/affiliate-content-creator fitness gear
```
*Simulated condition: First script draft omits disclosure; primary hook scores 6.2/10*

**Expected Behavior**:
- Stage 5 (Quality Reviewer): Returns FAIL (2 items: Check 2 — no script disclosure; Check 5 — hook score 6.2/10 < 7.0)
- Fix cycle 1: Adds disclosure to script DISCLOSURE section; replaces primary hook with best A/B variant (score 7.4/10)
- Stage 5 re-run: All 8 checks pass. Status: PASS.
- Stage 6: Proceeds normally.

**Expected Output**: Complete Content Package with disclosure present; hook score ≥ 7.0 in final review.

**Pass Criteria**:
- Fix cycle executes within the harness (no user intervention required)
- Re-run quality gate passes
- Final output shows the corrected hook and disclosure

**Fail Criteria**:
- Harness stops at FAIL without attempting fixes
- Fix cycle runs more than 2 times
- Final output still contains the quality gate failures

---

## Scenario 5: No Products Found in Niche

**Description**: Platform scan finds < 3 products in the user's specified niche. Harness should broaden the niche and retry, then ask the user if still insufficient.

**Input**:
```
/affiliate-content-creator underwater drone cameras
```
*Simulated condition: Only 1 product found in Stage 1*

**Expected Behavior**:
- Stage 1 first attempt: 1 product found ("underwater drone cameras" is too narrow)
- Stage 1 auto-retry: Broadens to "drones" → finds 4 products
- Continues with the closest match to the original intent
- Informs the user: "Your niche was broadened to 'drones' because only 1 product was found for 'underwater drone cameras'"

**Expected Output**: Content Package for a drone product with a note about niche broadening.

**Pass Criteria**:
- Auto-retry executes once with broadened niche
- User receives a clear explanation of the niche change
- Harness continues without manual intervention

**Fail Criteria**:
- Harness crashes when < 3 products are found
- Harness broadens niche silently without informing the user
- If after broadening still < 3 products, harness should ask the user — not crash

---

## Scenario 6: A/B Hook Variants — All Triggers Present

**Description**: Verify that sub-ab-title-generator produces 5 variants covering all 5 distinct psychological trigger types with no repeats.

**Input** (direct sub-skill test):
```
Invoke sub-ab-title-generator with:
  product_name: "Portable Mini Fan"
  primary_hook: "This tiny fan saved my summer"
  persona_card: {age: "18-30", pain_points: ["sweating on commute", "expensive AC bills", "poor sleep in heat"]}
  n_variants: 5
```

**Expected Output**:
- Variant A: Curiosity Gap trigger
- Variant B: Pain Agitation trigger
- Variant C: Aspiration/Transformation trigger
- Variant D: Social Proof trigger
- Variant E: Shock/Pattern Interrupt trigger
- Each variant ≤ 15 words
- No two variants > 70% similar in wording
- Each variant scores ≥ 6.0/10 on the weighted rubric

**Pass Criteria**:
- All 5 trigger types present
- All variants score ≥ 6.0/10
- No paraphrasing between variants
- A recommendation with rationale is provided

**Fail Criteria**:
- Two variants use the same trigger type
- Any variant > 15 words
- No recommendation provided

---

## Scenario 7: Vietnamese Market — Shopee Affiliate with Local Audience

**Description**: User targets the Vietnamese market on Shopee. Tests localization of audience targeting and platform preferences.

**Input**:
```
/affiliate-content-creator làm đẹp Vietnam Shopee
```
*(Mixed Vietnamese-English input, target: Vietnamese TikTok + Facebook)*

**Expected Behavior**:
- Stage 1: Scans Shopee Vietnam affiliate program for beauty/skincare trending items
- Stage 2: Audience persona is for Vietnamese women aged 18–35; pain points reference local concerns (sun protection for tropical climate, affordable skincare); posting times adjusted for VN timezone (GMT+7)
- Stage 3: Script written in English but with notes for Vietnamese dubbing/subtitle; hashtags include Vietnamese tags (#lamdepmoi, #lamdep)
- Stage 4–6: Normal flow

**Pass Criteria**:
- Shopee Vietnam is scanned in Stage 1
- Persona card references Vietnam as the primary geography
- Optimal posting time is in GMT+7
- Caption includes at least 1 Vietnamese-language hashtag

**Fail Criteria**:
- Audience targeting ignores the Vietnamese geography signal
- Posting times are in a non-VN timezone
- No attempt to include local platform hashtags

---

## Test Run Log

| Date | Scenario | Status | Notes |
|------|----------|--------|-------|
| (not yet run) | 1 | — | |
| (not yet run) | 2 | — | |
| (not yet run) | 3 | — | |
| (not yet run) | 4 | — | |
| (not yet run) | 5 | — | |
| (not yet run) | 6 | — | |
| (not yet run) | 7 | — | |
