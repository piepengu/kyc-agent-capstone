# Fix Google Custom Search API - Step by Step Guide

## Current Error
```
Requests to this API customsearch method google.customsearch.v1.CustomSearchService.List are blocked.
```

This means the API might be enabled but there are restrictions blocking it.

## Step-by-Step Fix

### Step 1: Verify Custom Search API is Enabled

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Make sure you're in the correct project (check top bar)
3. Navigate to **APIs & Services** → **Library**
4. Search for "Custom Search API"
5. Check status:
   - If it says **"Enable"** → Click it and wait 2-3 minutes
   - If it says **"Manage"** → It's enabled, proceed to Step 2

### Step 2: Check API Key Restrictions

1. Go to **APIs & Services** → **Credentials**
2. Find your API key (check your `.env` file or Google Cloud Console)
3. Click **Edit** (pencil icon)
4. Check **API restrictions**:
   - If "Restrict key" is selected, make sure **Custom Search API** is in the allowed list
   - If it's not listed, click **Add an API restriction** → Select **Custom Search API**
   - OR temporarily set to **"Don't restrict key"** for testing
5. Check **Application restrictions**:
   - If "None" → Good, proceed
   - If restricted → Temporarily set to **"None"** for testing, or add your IP/domain
6. Click **Save**

### Step 3: Verify Billing/Quota

1. Go to **APIs & Services** → **Dashboard**
2. Find **Custom Search API** in the list
3. Check:
   - **Status**: Should be "Enabled"
   - **Quota**: Should show 100 requests/day (free tier)
4. If you see billing warnings:
   - Go to **Billing** → **Account Management**
   - Ensure billing account is active (even if free tier)

### Step 4: Check API Key Permissions

1. Go to **IAM & Admin** → **Service Accounts**
2. Verify your API key has proper permissions
3. For Custom Search API, you typically don't need service accounts

### Step 5: Verify Search Engine ID

1. Go to [Google Custom Search Control Panel](https://programmablesearchengine.google.com/controlpanel/all)
2. Verify your search engine with ID `322c8536721cd40d8` exists
3. Check **Setup** → **Basics**:
   - **Sites to search**: Should be `*` (entire web) or specific sites
   - **Status**: Should be active

### Step 6: Test API Directly

After making changes, wait 2-3 minutes, then test:

```powershell
python main.py --name "Test Customer"
```

## Common Issues & Solutions

### Issue 1: API Key Restrictions Too Strict
**Solution**: Temporarily remove restrictions or add Custom Search API to allowed list

### Issue 2: Billing Account Not Linked
**Solution**: 
- Even for free tier, you may need a billing account
- Go to **Billing** → Link a billing account (won't charge for free tier)

### Issue 3: API Not Enabled in Correct Project
**Solution**: 
- Check you're in the right Google Cloud project
- The project ID should match: `gen-lang-client-0189571876` or `466331139671`

### Issue 4: Quota Exceeded
**Solution**: 
- Free tier: 100 searches/day
- Check usage in **APIs & Services** → **Dashboard** → **Custom Search API**
- Wait 24 hours for quota reset

## Quick Test Command

After fixing, test with:
```powershell
python -c "from googleapiclient.discovery import build; import os; from dotenv import load_dotenv; load_dotenv(); service = build('customsearch', 'v1', developerKey=os.getenv('GOOGLE_API_KEY')); result = service.cse().list(q='test', cx='322c8536721cd40d8', num=1).execute(); print('SUCCESS! API is working')"
```

## Alternative: Use Different Search Method

If Custom Search API continues to have issues, we can:
1. Use DuckDuckGo (free, no API key)
2. Use SerpAPI (free tier available)
3. Keep simulated search (works fine for competition)

Let me know what you find in the console!

