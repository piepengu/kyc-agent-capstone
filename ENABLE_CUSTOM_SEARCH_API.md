# Enable Google Custom Search API

## Quick Steps

The code detected that Custom Search API needs to be enabled. Here's how:

### Step 1: Enable the API

1. **Click this direct link** (from the error message):
   https://console.developers.google.com/apis/api/customsearch.googleapis.com/overview?project=466331139671

2. Or manually:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Navigate to **APIs & Services** → **Library**
   - Search for "Custom Search API"
   - Click **Enable**

### Step 2: Wait a Few Minutes

After enabling, wait 2-3 minutes for the API to propagate.

### Step 3: Test Again

Run the agent again:
```powershell
python main.py --name "Test Customer"
```

## Current Status

✅ **Code is ready** - SearchAgent will use real Google Custom Search once API is enabled  
✅ **Fallback works** - Currently using simulated search (still functional)  
✅ **Search Engine ID configured** - `322c8536721cd40d8` is set up

## Free Tier

- **100 free searches per day**
- Perfect for development and competition
- No credit card required for free tier

## What Happens After Enabling

Once enabled, you'll see:
- `[+] SearchAgent initialized with Google Custom Search (CX: 322c853672...)`
- Real search results from Google
- Actual news articles and web pages

The agent will automatically switch from simulated to real search once the API is enabled!

