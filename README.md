# 🚀 AI-Powered Job Scraper API

A modern, AI-powered job scraping API that uses **FREE local AI** (Ollama) to intelligently extract structured job data from any job posting website.

## ✨ Features

- 🤖 **FREE AI-powered extraction** using Ollama (Llama 3.2)
- 📊 **Intelligent data extraction** - no hardcoded selectors needed
- 🗄️ **MongoDB integration** for data storage
- 🔗 **RESTful API** for easy integration with n8n workflows
- 🛡️ **Error handling** and fallback mechanisms
- ⚡ **Fast and reliable** with automatic deduplication

## 🎯 What It Extracts

- Job title and company
- Location and employment type
- Salary information
- Seniority level
- Technical skills (Python, React, AWS, etc.)
- Soft skills (Communication, Leadership, etc.)
- Comprehensive job description
- Posting date and job link

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    n8n      │───▶│  API Server │───▶│   Ollama    │───▶│  MongoDB    │
│ Workflow    │    │    (Flask)  │    │ (Local AI)  │    │ (Database)  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install & Start Ollama

```bash
# Windows
winget install Ollama.Ollama
ollama pull llama3.2
```

### 3. Install & Start MongoDB

```bash
# Windows
winget install MongoDB.Server
# MongoDB will start automatically
```

### 4. Start the API Server

```bash
python api_server_clean.py
```

The API will be available at `http://localhost:5000`

## 📡 API Endpoints

### POST /scrape

Scrape a job from URL and save to database.

**Request:**

```json
{
  "job_url": "https://example.com/job-posting"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "title": "Senior Python Developer",
    "company": "Tech Corp",
    "location": "Remote",
    "employment_type": "Full-time",
    "salary": "80000$-120000$",
    "seniority": "Senior",
    "tech_skills": ["Python", "Django", "AWS", "Docker"],
    "soft_skills": ["Communication", "Leadership"],
    "description": "Full job description...",
    "date_posted": "2025-08-16",
    "job_link": "https://example.com/job-posting"
  },
  "message": "Job saved successfully"
}
```

### GET /health

Check API and database status.

### GET /jobs

Get recent jobs from database.

- Query params: `limit` (default: 10), `skip` (default: 0)

## 🔧 Configuration

Environment variables can be set in a `.env` file:

```bash
# API Configuration
PORT=5000
DEBUG=false

# Database Configuration
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=job_scraper
COLLECTION_NAME=jobs
```

## 🤝 n8n Integration

### Workflow Setup:

```
HTTP Request → MongoDB → Google Sheets → NoOp
```

### HTTP Request Node:

- **Method:** POST
- **URL:** `http://localhost:5000/scrape`
- **Body:** `{"job_url": "{{YOUR_JOB_URL}}"}`

## 📁 Project Structure

```
├── api_server_clean.py    # Main API server
├── scraper_core.py        # Core scraping logic
├── database.py            # MongoDB operations
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🛡️ Error Handling

- **AI fallback**: If AI extraction fails, uses regex-based fallback
- **Validation**: Input validation for URLs and data
- **Logging**: Comprehensive logging for debugging
- **Graceful degradation**: Continues working even if some components fail

## 🔄 Data Flow

1. **n8n** sends job URL to API
2. **API** uses Selenium to fetch the webpage
3. **AI (Ollama)** intelligently extracts structured data
4. **MongoDB** stores the job data (with deduplication)
5. **API** returns structured JSON to n8n
6. **n8n** can then save to Google Sheets, send notifications, etc.

## 🎯 Why This Approach?

- **No API costs** - Uses free local AI (Ollama)
- **No hardcoded selectors** - AI adapts to any website structure
- **Future-proof** - Works with new job sites without code changes
- **Privacy-focused** - All processing happens locally
- **Scalable** - Can handle high volume with proper infrastructure

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.
