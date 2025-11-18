# Risk Assessment Guide

## Risk Level Values

The KYC Bot uses **three risk levels**:

1. **LOW** - Minimal risk, standard due diligence sufficient
2. **MEDIUM** - Moderate risk, enhanced due diligence recommended
3. **HIGH** - Significant risk, requires immediate attention and enhanced monitoring

## Current Risk Assessment Method

**Important**: Currently, risk levels are determined by **Gemini AI** based on the search results and watchlist findings. The AI analyzes the context and makes a judgment call. This means:

- Risk assessments are **context-aware** and consider the full picture
- The AI looks at the **nature** of findings, not just their presence
- **No explicit rules** are currently hardcoded - it's AI-driven analysis

## How Risk Levels Are Determined

The AnalysisAgent sends the following information to Gemini:

1. **Adverse Media Search Results** - News articles, reports mentioning the customer
2. **Watchlist Check Results** - Whether the customer appears on sanctions lists

Gemini then analyzes:
- The **severity** of adverse media findings
- The **relevance** of findings to financial crime
- Whether the customer is a **victim** vs. **perpetrator**
- The **recency** and **credibility** of sources
- **Watchlist matches** (automatic HIGH risk if matched)

## Typical Risk Assessment Criteria

### LOW Risk Indicators:
- ✅ No watchlist matches
- ✅ No adverse media, or only positive/neutral news
- ✅ Adverse media is unrelated to financial crime
- ✅ Customer is a victim (e.g., identity theft, deepfake scams)
- ✅ Findings are old/outdated
- ✅ False positives (different person with same name)

**Example**: Professional athlete with only sports-related news, or person whose name was used in scams without their knowledge.

### MEDIUM Risk Indicators:
- ⚠️ No watchlist matches, BUT:
- ⚠️ Adverse media mentions fraud, money laundering, or financial crimes
- ⚠️ Ambiguous findings requiring further investigation
- ⚠️ Recent news about financial irregularities
- ⚠️ Association with high-risk individuals or entities
- ⚠️ Name similarity to known criminals (potential false positive)

**Example**: Shakira might get MEDIUM if search results mention:
- Tax evasion allegations
- Financial investigations
- Legal disputes involving money
- Association with suspicious financial activities

### HIGH Risk Indicators:
- 🚨 **Watchlist match** (automatic HIGH)
- 🚨 Direct involvement in financial crimes
- 🚨 Active sanctions or legal restrictions
- 🚨 Recent convictions for financial crimes
- 🚨 Multiple serious adverse media findings
- 🚨 Clear evidence of money laundering or fraud

**Example**: Person on OFAC sanctions list, or multiple recent news articles about fraud convictions.

## Why Shakira Might Get MEDIUM Risk

Shakira (the Colombian singer) might receive MEDIUM risk because:

1. **Tax-related issues**: She has been involved in tax evasion cases in Spain
2. **Financial investigations**: News about financial irregularities
3. **Legal disputes**: High-profile cases involving money
4. **Recent adverse media**: Ongoing or recent financial-related news

Even though she's not on watchlists, the **adverse media about financial matters** triggers MEDIUM risk because:
- It's relevant to financial compliance
- It's recent and credible
- It involves significant amounts of money
- It requires Enhanced Due Diligence to verify current status

## Improving Risk Assessment

### Option 1: Add Explicit Rules to Prompt (Recommended)

We can enhance the prompt in `agents.py` to include explicit risk assessment criteria:

```python
prompt = f"""...
RISK ASSESSMENT CRITERIA:
- LOW: No watchlist matches AND (no adverse media OR only unrelated/positive news OR customer is a victim)
- MEDIUM: No watchlist matches BUT adverse media mentions fraud, money laundering, tax issues, or financial crimes
- HIGH: Watchlist match OR multiple serious financial crime findings OR recent convictions

Please assess risk based on these criteria..."""
```

### Option 2: Rule-Based Risk Scoring

We could implement a scoring system:
- Watchlist match: +100 points (automatic HIGH)
- Fraud mentions: +30 points
- Money laundering: +40 points
- Tax issues: +20 points
- Sanctions mentions: +25 points
- Recent findings (< 2 years): +10 points
- Multiple findings: +15 points

Then map scores to risk levels:
- 0-20: LOW
- 21-60: MEDIUM
- 61+: HIGH

### Option 3: Hybrid Approach

Combine rule-based scoring with AI analysis for nuanced cases.

## Current Implementation

**File**: `agents.py`, lines 288-306

The current prompt asks Gemini to:
1. Analyze the information
2. Determine risk level (LOW, MEDIUM, or HIGH)
3. Provide reasoning

**No explicit rules are provided** - Gemini uses its training to make the assessment.

## Recommendations

1. **For Competition**: The current AI-driven approach is acceptable as it shows intelligent analysis
2. **For Production**: Add explicit risk criteria to the prompt for consistency
3. **For Transparency**: Document the criteria (this file) so users understand the logic

## Testing Risk Levels

To test different risk levels:

```powershell
# Should be LOW - professional athlete
.\run_agent.ps1 -Name "Grigor Dimitrov"

# Might be MEDIUM - tax/financial issues
.\run_agent.ps1 -Name "Shakira"

# Should be MEDIUM - suspicious name
.\run_agent.ps1 -Name "Pablo Escubar"

# Should be LOW - common name, no issues
.\run_agent.ps1 -Name "John Smith"
```

## Viewing Risk Assessment Details

After running an investigation, check the report for:
- **Risk Level** section
- **Key Findings** - explains why the risk level was assigned
- **Recommendations** - what actions to take

The log file also captures the risk level:
```powershell
Get-Content logs\kyc_bot_$(Get-Date -Format "yyyyMMdd").log | Select-String "Risk level"
```

