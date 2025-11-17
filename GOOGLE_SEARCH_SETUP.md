# Google Custom Search Engine Setup Guide

## What is Google Custom Search Engine?

Google Custom Search Engine (CSE) allows you to create a search engine that searches specific websites or the entire web. You need:
1. **Search Engine ID (CX)** - Identifies your custom search engine
2. **API Key** - You already have this! (for Google APIs)

## Free Tier Information

✅ **YES, Google Custom Search is FREE for:**
- Up to **100 search queries per day** (free tier)
- Perfect for development and testing
- For the competition, this should be more than enough

## How to Check if You Have a Search Engine ID

You likely **don't have one yet** - you need to create it. Here's how to check:

1. Go to [Google Custom Search](https://programmablesearchengine.google.com/)
2. Sign in with your Google account
3. Check if you have any existing search engines listed

## How to Create a Free Google Custom Search Engine

### Step 1: Create the Search Engine

1. Go to: https://programmablesearchengine.google.com/controlpanel/create
2. Sign in with your Google account (same one you used for the API key)
3. Fill in the form:
   - **Sites to search**: Enter `*` (asterisk) to search the entire web
   - **Name**: "KYC Bot Search Engine" (or any name)
   - **Language**: English
4. Click **Create**

### Step 2: Get Your Search Engine ID (CX)

1. After creating, you'll see your search engine in the control panel
2. Click on your search engine
3. Go to **Setup** → **Basics**
4. You'll see **Search engine ID** - this is your CX value
   - Format: `xxxxxxxxxxxxxxxxxxxxxxxxx:xxxxxxxxxx`
   - Example: `017576662512468239146:omuauf_lfve`

### Step 3: Enable Custom Search API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services** → **Library**
3. Search for "Custom Search API"
4. Click **Enable**

### Step 4: Add to Your .env File

Add the Search Engine ID to your `.env` file:

```bash
GOOGLE_API_KEY=your_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_cx_value_here
```

## Alternative: Use Free Search APIs

If you don't want to set up Google Custom Search, here are free alternatives:

### Option 1: DuckDuckGo (Free, No API Key Needed)
- Completely free
- No rate limits for reasonable use
- Easy to implement
- Good for demo purposes

### Option 2: SerpAPI (Free Tier)
- 100 free searches per month
- Requires signup
- More structured results

### Option 3: Keep Simulated Search
- For competition demo, simulated search is fine
- Focus on showing the architecture and workflow
- Judges care more about the agent design than real search results

## Recommendation for Competition

**For the competition deadline (Nov 30th), I recommend:**

1. **Quick Option**: Use DuckDuckGo search (free, no setup needed)
   - Fast to implement
   - Shows real search functionality
   - No API limits for demo

2. **If you have time**: Set up Google Custom Search
   - More professional
   - Better integration with Google ecosystem
   - 100 free searches/day is plenty

3. **Simplest**: Keep simulated search
   - Focus on agent architecture
   - Judges care more about multi-agent design
   - Can mention it's ready for real API integration

## Next Steps

Would you like me to:
1. Implement DuckDuckGo search (fastest, free)?
2. Help you set up Google Custom Search?
3. Enhance the simulated search with better mock data?

Let me know which option you prefer!

