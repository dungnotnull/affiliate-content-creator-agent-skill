# API Authentication Setup — affiliate-content-creator

This document explains how to set up API credentials for TikTok and Facebook posting via the `sub-platform-poster` skill.

> **Security**: Never hardcode API tokens in skill files or commit them to version control. Always use environment variables or a `.env` file excluded by `.gitignore`.

---

## TikTok Content Posting API

### Prerequisites
- A TikTok Developer Account (https://developers.tiktok.com)
- A TikTok For Business account for the posting user
- The app must have **Video Upload** (`user.info.basic`, `video.upload`, `video.publish`) scopes approved by TikTok

### Setup Steps

1. **Create a TikTok App**
   - Go to [TikTok Developer Portal](https://developers.tiktok.com/)
   - Sign in → **My Apps** → **Create App**
   - Select **Production App**
   - Add scopes: `user.info.basic`, `video.upload`, `video.publish`
   - Set the redirect URI (your local callback for OAuth)

2. **Get Access Token (OAuth 2.0 PKCE Flow)**
   ```
   # Step 1: Generate auth URL
   https://www.tiktok.com/v2/auth/authorize/
     ?client_key={CLIENT_KEY}
     &scope=user.info.basic,video.upload,video.publish
     &response_type=code
     &redirect_uri={REDIRECT_URI}
     &state={RANDOM_STATE}
     &code_challenge_method=S256
     &code_challenge={CODE_CHALLENGE}

   # Step 2: Exchange auth code for access token
   POST https://open-api.tiktok.com/v2/oauth/token/
   Headers: Content-Type: application/x-www-form-urlencoded
   Body:
     client_key={CLIENT_KEY}
     client_secret={CLIENT_SECRET}
     code={AUTH_CODE}
     grant_type=authorization_code
     redirect_uri={REDIRECT_URI}
     code_verifier={CODE_VERIFIER}

   # Response:
   {
     "access_token": "...",
     "expires_in": 86400,  # 24 hours
     "refresh_token": "...",
     "open_id": "..."
   }
   ```

3. **Token Refresh**
   TikTok access tokens expire after 24 hours. The `sub-platform-poster` skill attempts auto-refresh:
   ```
   POST https://open-api.tiktok.com/v2/oauth/token/
   Body:
     client_key={CLIENT_KEY}
     client_secret={CLIENT_SECRET}
     grant_type=refresh_token
     refresh_token={REFRESH_TOKEN}
   ```

4. **Environment Variables**
   ```bash
   export TIKTOK_CLIENT_KEY="your_client_key"
   export TIKTOK_CLIENT_SECRET="your_client_secret"
   export TIKTOK_ACCESS_TOKEN="your_access_token"
   export TIKTOK_REFRESH_TOKEN="your_refresh_token"
   export TIKTOK_OPEN_ID="your_open_id"
   ```

### Rate Limits
- Standard tier: 50 video uploads per day, 10 per hour
- To increase: Apply for higher tier via TikTok Developer Portal

---

## Meta Graph API (Facebook Reels)

### Prerequisites
- A Facebook Developer Account (https://developers.facebook.com)
- A Facebook Business Page (for posting Reels)
- A Meta App with **Reels Publishing** permissions

### Setup Steps

1. **Create a Meta App**
   - Go to [Meta Developer Portal](https://developers.facebook.com/)
   - **My Apps** → **Create App** → **Business**
   - Add **Facebook Pages API** product
   - Add **Instagram Graph API** product (if posting to Instagram Reels)

2. **Get Page Access Token (OAuth 2.0)**
   ```
   # Step 1: Login dialog
   https://www.facebook.com/v19.0/dialog/oauth?
     client_id={APP_ID}
     redirect_uri={REDIRECT_URI}
     scope=pages_show_list,pages_read_engagement,pages_manage_posts
     state={RANDOM_STATE}

   # Step 2: Exchange code for user access token
   GET https://graph.facebook.com/v19.0/oauth/access_token?
     client_id={APP_ID}
     redirect_uri={REDIRECT_URI}
     client_secret={APP_SECRET}
     code={AUTH_CODE}

   # Step 3: Get page access token (from user token)
   GET https://graph.facebook.com/v19.0/{USER_ID}/accounts?
     access_token={USER_ACCESS_TOKEN}
   # Pick the page you want to post to → get page_access_token

   # Step 4: Extend to long-lived token (60 days)
   GET https://graph.facebook.com/v19.0/oauth/access_token?
     grant_type=fb_exchange_token
     client_id={APP_ID}
     client_secret={APP_SECRET}
     fb_exchange_token={PAGE_ACCESS_TOKEN}
   ```

3. **Environment Variables**
   ```bash
   export META_APP_ID="your_app_id"
   export META_APP_SECRET="your_app_secret"
   export META_PAGE_ID="your_page_id"
   export META_ACCESS_TOKEN="your_long_lived_page_access_token"
   ```

### Rate Limits
- Standard tier: 100 Reels posts per 24 hours per page
- 1 Reels post per 5 minutes minimum interval

---

## Graceful Degradation

If any API credentials are missing or expired, `sub-platform-poster` **does not fail** — it generates a manual-post package. This means you can:

- Use the skill without any API setup during content creation (Stages 1–5)
- Only configure credentials when you want automatic posting (Stage 6)
- See the manual-post package format before committing to API integration

To test Stage 6 without credentials, set no environment variables — the poster will detect the missing credentials and produce a manual-post package automatically.

---

## Testing Authentication

Use these cURL commands to verify your credentials before running the harness:

### TikTok
```bash
# Check token validity
curl -s -X GET "https://open-api.tiktok.com/v2/user/info/\
  ?fields=open_id,display_name,avatar_url" \
  -H "Authorization: Bearer $TIKTOK_ACCESS_TOKEN" | jq .

# Expected: JSON response with user info (not 401/403 error)
```

### Facebook
```bash
# Check page token
curl -s -X GET "https://graph.facebook.com/v19.0/$META_PAGE_ID\
  ?fields=name,access_token&access_token=$META_ACCESS_TOKEN" | jq .

# Expected: JSON response with page name (not 400 error)
```

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| TikTok returns 401 | Token expired | Run refresh token flow; update env vars |
| TikTok returns 403 | Missing scope | Re-authorize app with `video.upload` + `video.publish` |
| Facebook returns 400/403 | Token expired or wrong page ID | Re-run long-lived token exchange |
| Facebook returns 400 (invalid page ID) | Page ID is personal profile (not Business page) | Use a Business Page ID, not personal profile |
| "App not approved for this scope" | TikTok/Meta review pending | Submit app for review with video walkthrough |
| Rate limited (429) | Hit daily upload cap | Wait 24h or request higher tier |
