# Quick Fix: Enable Custom Search API

## The Problem
The error message says: **"Custom Search API has not been used in project 466331139671 before or it is disabled"**

## The Solution (2 Steps)

### Step 1: Enable the API

**Click this direct link:**
https://console.developers.google.com/apis/api/customsearch.googleapis.com/overview?project=466331139671

1. You'll see a page about Custom Search API
2. Click the big blue **"ENABLE"** button
3. Wait 2-3 minutes for it to activate

### Step 2: Test Again

After waiting 2-3 minutes, run:
```powershell
python main.py --name "Test Customer"
```

You should see real search results instead of simulated ones!

## What to Look For

After enabling, when you run the agent, you should see:
- `[+] Found X real search results` (instead of simulated)
- Actual news articles and web pages in the results

## If It Still Doesn't Work

1. **Check API Key Restrictions:**
   - Go to [Credentials](https://console.cloud.google.com/apis/credentials)
   - Click on your API key
   - Under "API restrictions", make sure "Custom Search API" is allowed
   - Or temporarily set to "Don't restrict key"

2. **Verify Billing:**
   - Even for free tier, you may need a billing account linked
   - Go to [Billing](https://console.cloud.google.com/billing)
   - Link a billing account (won't charge for free tier)

## Free Tier Limits

- ✅ **100 free searches per day**
- ✅ No credit card required for free tier
- ✅ Perfect for competition use

