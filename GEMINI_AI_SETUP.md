# Gemini AI Integration Setup

## 🎯 Why Gemini AI?

Your scraper was returning generic data like:

- Title: "Job Position"
- Company: "Company"
- Salary: "Not specified"
- Skills: []

Gemini AI will extract **real data** from gamma.app URLs!

## 🚀 Quick Setup (2 minutes)

### Step 1: Get Your FREE Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the generated key (starts with `AIza...`)

### Step 2: Set Up the API Key

**Option A: Use the Setup Script**

```bash
.\setup-gemini.bat
```

**Option B: Manual Setup**

```bash
# Windows
setx GEMINI_API_KEY "your_api_key_here"

# Linux/Mac
export GEMINI_API_KEY="your_api_key_here"
```

### Step 3: Restart Containers

```bash
docker-compose down
docker-compose up -d
```

## 🔥 How It Works

### Before Gemini AI:

```json
{
  "title": "Job Position",
  "company": "Company",
  "salary": "Not specified",
  "tech_skills": [],
  "extraction_method": "intelligent_content_parsing"
}
```

### After Gemini AI:

```json
{
  "title": "Senior Data Scientist",
  "company": "TechCorp Inc",
  "salary": "$120,000 - $160,000",
  "tech_skills": ["Python", "TensorFlow", "SQL", "AWS"],
  "requirements": ["5+ years ML experience", "PhD preferred"],
  "extraction_method": "gemini_ai_extraction"
}
```

## 🎯 Smart Fallback System

1. **First**: Traditional Chrome scraping tries
2. **If generic data detected**: Gemini AI kicks in automatically
3. **If Chrome fails**: Gemini AI analyzes URL directly
4. **Result**: Real job data every time!

## 🧠 Gemini AI Features

- **URL Analysis**: Extracts job details from gamma.app URL structure
- **Content Parsing**: Analyzes actual page content when available
- **Smart Enhancement**: Combines URL patterns with AI reasoning
- **Comprehensive Extraction**:
  - Real job titles
  - Actual company names
  - Genuine salary ranges
  - Detailed requirements
  - Specific tech skills
  - Accurate seniority levels

## 📊 Detection Logic

Gemini AI activates when traditional scraping returns:

- Generic titles like "Job Position"
- Generic companies like "Company"
- Empty skills arrays
- "Not specified" values
- Missing requirements/benefits

## 🔧 Environment Variables

The system uses these environment variables:

- `GEMINI_API_KEY`: Your Google AI API key
- Auto-loaded in Docker Compose
- Falls back gracefully if not set

## ✅ Verification

After setup, your scraper will:

1. Try traditional extraction first
2. Detect if data is generic
3. Automatically use Gemini AI
4. Return detailed, accurate job data
5. Show `"extraction_method": "gemini_ai_extraction"`

## 💡 Tips

- **Free Tier**: 60 requests per minute (plenty for your use case)
- **Cost**: First 1000 requests/day are FREE
- **Fallback**: System works without Gemini (with basic data)
- **Performance**: Gemini responses typically take 2-5 seconds

## 🚨 Troubleshooting

**"Gemini AI not enabled"**:

- Check API key is set: `echo $GEMINI_API_KEY`
- Restart containers after setting key

**"Gemini extraction failed"**:

- Verify API key is valid
- Check Google AI Studio quotas
- System will fallback to traditional scraping

## 🎉 Ready!

Your email automation now has AI-powered extraction that will get real job data from any gamma.app URL!
