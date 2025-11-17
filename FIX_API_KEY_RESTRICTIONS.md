# Fix API Key Restrictions for Custom Search API

## Current Error
```
Requests to this API customsearch method google.customsearch.v1.CustomSearchService.List are blocked.
```

**The API is enabled, but your API key is restricted and doesn't allow Custom Search API.**

## Quick Fix: Update API Key Restrictions

### Step 1: Go to Credentials Page

1. **Click this link** (you're already signed in):
   https://console.cloud.google.com/apis/credentials?project=gen-lang-client-0189571876

2. Or manually navigate:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Click **APIs & Services** → **Credentials**

### Step 2: Edit Your API Key

1. Find your API key (check your `.env` file or Google Cloud Console)
2. Click the **pencil icon** (Edit) next to it

### Step 3: Update API Restrictions

1. Scroll down to **"API restrictions"** section
2. You'll see one of these options:
   - **"Don't restrict key"** (recommended for testing)
   - **"Restrict key"** (with a list of allowed APIs)

3. **Choose one:**
   
   **Option A: Remove Restrictions (Easiest for Testing)**
   - Select **"Don't restrict key"**
   - Click **Save**
   - ⚠️ **Note:** This allows all APIs. For production, you should restrict it.

   **Option B: Add Custom Search API to Allowed List**
   - Select **"Restrict key"**
   - Click **"Select APIs"** dropdown
   - Check the box for **"Custom Search API"**
   - If you see other APIs already checked, keep them checked
   - Click **OK**
   - Click **Save**

### Step 4: Check Application Restrictions (Optional)

1. Scroll to **"Application restrictions"** section
2. For testing, set to **"None"**
3. For production, you can restrict by:
   - IP addresses
   - HTTP referrers (websites)
   - Android apps
   - iOS apps

### Step 5: Wait and Test

1. **Wait 1-2 minutes** for changes to propagate
2. Test the agent:
   ```powershell
   python main.py --name "Test Customer"
   ```

## What You Should See After Fixing

✅ **Success indicators:**
- `[+] Found X real search results` (instead of simulated)
- No error messages about blocked requests
- Actual web page titles and snippets in results

❌ **If still blocked:**
- Check you saved the changes
- Wait another 2-3 minutes
- Verify you're editing the correct API key
- Check billing account is linked (even for free tier)

## Security Note

For the competition/demo:
- **"Don't restrict key"** is fine for testing
- After the competition, restrict the key to only needed APIs

For production:
- Always restrict API keys to specific APIs
- Add application restrictions (IP/referrer)
- Rotate keys regularly

## Alternative: Create New Unrestricted API Key

If you want to keep your current key restricted, create a new one:

1. Go to **Credentials** page
2. Click **+ CREATE CREDENTIALS** → **API key**
3. Copy the new key
4. Update your `.env` file:
   ```
   GOOGLE_API_KEY=your_new_key_here
   ```
5. Set restrictions on the new key as needed

## Still Having Issues?

If it still doesn't work after fixing restrictions:

1. **Check billing:**
   - Go to [Billing](https://console.cloud.google.com/billing)
   - Ensure a billing account is linked (won't charge for free tier)

2. **Verify API is enabled:**
   - Go to [API Library](https://console.cloud.google.com/apis/library)
   - Search "Custom Search API"
   - Should show "Enabled" status

3. **Check quota:**
   - Free tier: 100 searches/day
   - Go to [Dashboard](https://console.cloud.google.com/apis/dashboard)
   - Check Custom Search API usage

Let me know once you've updated the restrictions and we can test again!

