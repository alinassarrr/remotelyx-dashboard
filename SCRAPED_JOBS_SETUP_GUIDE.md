# 🤖 RemotelyX Dashboard - Scraped Jobs Integration Guide

This guide shows you how to integrate your job scraper data with the RemotelyX Dashboard backend.

## 📋 **What's New**

Your backend now supports:

- ✅ **Bulk job import** from scraper data
- ✅ **Duplicate detection** and automatic updates
- ✅ **Enhanced job schema** with scraper-specific fields
- ✅ **Skills categorization** (tech_skills vs soft_skills)
- ✅ **Flexible salary handling** (string + numeric ranges)
- ✅ **Import statistics** and monitoring

## 🚀 **Quick Setup**

### 1. Run Database Migration

```bash
# Navigate to server directory
cd server

# Run the migration to update job schema
./run_migration.sh add_scraped_job_fields

# If you need to rollback
./run_migration.sh add_scraped_job_fields down
```

### 2. Start the Backend Server

```bash
# Make sure you're in the server directory
cd server

# Start the development server
./run_dev.sh
```

The server will be available at `http://localhost:8000`

## 📊 **New API Endpoints**

### 🔄 **Bulk Import Jobs**

Import multiple jobs from your scraper:

```http
POST /api/v1/scraped-jobs/import
Content-Type: application/json

{
  "jobs": [
    {
      "data": {
        "company": "Gamma",
        "date_posted": "Not specified",
        "description": "We are looking for a highly skilled Full-Stack Developer...",
        "employment_type": "Full-time",
        "job_link": "https://gamma.app/docs/full-stack-developer...",
        "location": "Remote",
        "salary": "$2,500+",
        "scraped_at": "Sun, 17 Aug 2025 00:02:43 GMT",
        "seniority": "Mid",
        "soft_skills": ["communication", "leadership", "teamwork"],
        "tech_skills": ["React.js", "Next.js", "Node.js", "Nest.js"],
        "title": "Full Stack Developer - IC",
        "updated_at": "Sun, 17 Aug 2025 00:02:43 GMT"
      },
      "message": "Job updated successfully",
      "scraped_at": "2025-08-17T00:02:43.608904",
      "success": true
    }
  ]
}
```

**Response:**

```json
{
  "total_jobs": 1,
  "successful_imports": 1,
  "failed_imports": 0,
  "created_jobs": ["64f123456789012345678901"],
  "updated_jobs": [],
  "errors": [],
  "message": "Successfully imported all 1 jobs"
}
```

### 📝 **Single Job Import**

Import one job at a time:

```http
POST /api/v1/scraped-jobs/import/single
Content-Type: application/json

{
  "data": {
    "company": "TechStartup",
    "title": "Senior Frontend Developer",
    "location": "Remote",
    "salary": "$4,000-6,000",
    // ... other fields
  },
  "success": true,
  "message": "Job scraped successfully",
  "scraped_at": "2025-08-17T12:00:00.000000"
}
```

### 📈 **Import Statistics**

Monitor your scraping progress:

```http
GET /api/v1/scraped-jobs/stats
```

**Response:**

```json
{
  "total_jobs": 150,
  "scraped_jobs": 120,
  "manual_jobs": 30,
  "recently_scraped": 25,
  "scraping_coverage": 80.0
}
```

## 🔧 **Enhanced Job Schema**

### **New Fields Added:**

| Field             | Type     | Description           | Example                   |
| ----------------- | -------- | --------------------- | ------------------------- |
| `description`     | string   | Full job description  | "We are looking for..."   |
| `employment_type` | string   | Employment type       | "Full-time", "Part-time"  |
| `job_link`        | string   | Original job URL      | "https://company.com/job" |
| `salary`          | string   | Salary as text        | "$2,500+", "Competitive"  |
| `date_posted`     | string   | Original posting date | "Not specified"           |
| `tech_skills`     | array    | Technical skills      | ["React", "Node.js"]      |
| `soft_skills`     | array    | Soft skills           | ["communication"]         |
| `scraped_at`      | datetime | When job was scraped  | ISO timestamp             |

### **Automatic Processing:**

1. **Skills Combination:** `tech_skills` + `soft_skills` → `skills` (for backward compatibility)
2. **Salary Parsing:** `"$2,500+"` → `salary_min: 2500, salary_max: 5000`
3. **Location Type:** `"Remote"` → `type: "remote"`
4. **Seniority Normalization:** `"Mid"` → `"mid"`

## 🛠️ **Integration Examples**

### **Python Scraper Integration**

```python
import requests
import json

# Your scraped job data
scraped_jobs = [
    {
        "data": {
            "company": "Gamma",
            "title": "Full Stack Developer - IC",
            "location": "Remote",
            "salary": "$2,500+",
            "tech_skills": ["React.js", "Node.js"],
            "soft_skills": ["communication", "teamwork"],
            # ... other fields from your scraper
        },
        "success": True,
        "message": "Job scraped successfully",
        "scraped_at": "2025-08-17T00:02:43.608904"
    }
]

# Send to RemotelyX API
response = requests.post(
    "http://localhost:8000/api/v1/scraped-jobs/import",
    json={"jobs": scraped_jobs},
    headers={"Content-Type": "application/json"}
)

result = response.json()
print(f"Imported {result['successful_imports']} jobs successfully")
```

### **JavaScript/Node.js Integration**

```javascript
const axios = require("axios");

async function importScrapedJobs(jobs) {
  try {
    const response = await axios.post(
      "http://localhost:8000/api/v1/scraped-jobs/import",
      { jobs },
      { headers: { "Content-Type": "application/json" } }
    );

    console.log("Import result:", response.data);
    return response.data;
  } catch (error) {
    console.error("Import failed:", error.response?.data || error.message);
    throw error;
  }
}

// Usage
const scrapedJobs = [
  /* your scraped job data */
];
importScrapedJobs(scrapedJobs);
```

### **cURL Example**

```bash
curl -X POST http://localhost:8000/api/v1/scraped-jobs/import \
  -H "Content-Type: application/json" \
  -d '{
    "jobs": [{
      "data": {
        "company": "Gamma",
        "title": "Full Stack Developer - IC",
        "location": "Remote",
        "salary": "$2,500+",
        "tech_skills": ["React.js", "Node.js"],
        "soft_skills": ["communication", "teamwork"],
        "description": "We are looking for...",
        "employment_type": "Full-time",
        "job_link": "https://example.com/job",
        "seniority": "Mid",
        "scraped_at": "Sun, 17 Aug 2025 00:02:43 GMT",
        "updated_at": "Sun, 17 Aug 2025 00:02:43 GMT",
        "date_posted": "Not specified"
      },
      "success": true,
      "message": "Job scraped successfully",
      "scraped_at": "2025-08-17T00:02:43.608904"
    }]
  }'
```

## 🔍 **Duplicate Detection**

The system automatically detects duplicates based on:

- **Company name** (case-insensitive)
- **Job title** (case-insensitive)
- **Job link** (exact match, if provided)

**Behavior:**

- ✅ **Found duplicate:** Updates existing job with new data
- ✅ **No duplicate:** Creates new job entry
- ✅ **Logs all actions:** Check server logs for detailed import information

## 📱 **Frontend Integration**

Your Streamlit frontend in the `client/` directory should continue working as before. The new fields will be available when you fetch jobs:

```python
# In your Streamlit app (client/app.py)
response = requests.get("http://localhost:8000/api/v1/jobs")
jobs = response.json()

for job in jobs:
    st.write(f"**{job['title']}** at {job['company']}")
    if job.get('salary'):
        st.write(f"💰 Salary: {job['salary']}")
    if job.get('tech_skills'):
        st.write(f"🛠️ Tech Skills: {', '.join(job['tech_skills'])}")
    if job.get('job_link'):
        st.write(f"🔗 [Apply Here]({job['job_link']})")
```

## 🧪 **Testing with Postman**

1. **Import the updated collection:** `RemotelyX_API_Updated.postman_collection.json`
2. **Test the new endpoints:**
   - Bulk Import: `POST /api/v1/scraped-jobs/import`
   - Single Import: `POST /api/v1/scraped-jobs/import/single`
   - Statistics: `GET /api/v1/scraped-jobs/stats`

## 📈 **Monitoring & Analytics**

### **Check Import Status**

```http
GET /api/v1/scraped-jobs/stats
```

### **View Recent Activity**

Check server logs for detailed import information:

```bash
# In server directory
tail -f logs/app.log  # or wherever your logs are stored
```

### **Database Verification**

```bash
# Connect to MongoDB
mongo remotelyx_dashboard

# Check scraped jobs
db.jobs.find({"scraped_at": {$exists: true}}).count()

# View recent scraped jobs
db.jobs.find({"scraped_at": {$exists: true}}).sort({"scraped_at": -1}).limit(5)
```

## 🚨 **Error Handling**

### **Common Issues & Solutions**

**❌ Invalid date format**

```json
{
  "error": "Invalid date format in scraped_at field"
}
```

**✅ Solution:** Ensure dates are in format: `"Sun, 17 Aug 2025 00:02:43 GMT"` or ISO format

**❌ Missing required fields**

```json
{
  "error": "Missing required field: company"
}
```

**✅ Solution:** Ensure `company`, `title`, `location` are always provided

**❌ Duplicate detection failed**

```json
{
  "error": "Database connection error"
}
```

**✅ Solution:** Check MongoDB is running and accessible

## 🔄 **Rollback Instructions**

If you need to rollback the changes:

```bash
# Rollback database migration
cd server
./run_migration.sh add_scraped_job_fields down

# This will remove the new fields from existing jobs
```

## 📋 **Summary**

✅ **Database schema updated** with scraped job fields  
✅ **New API endpoints** for bulk and single job import  
✅ **Duplicate detection** with automatic updates  
✅ **Enhanced skills categorization** (tech vs soft)  
✅ **Flexible salary handling** (text + numeric)  
✅ **Import monitoring** and statistics  
✅ **Backward compatibility** maintained  
✅ **Migration scripts** for easy deployment

Your scraper can now send data directly to the RemotelyX Dashboard backend, and the frontend will automatically display the enhanced job information! 🚀

## 🆘 **Need Help?**

- **API Documentation:** Visit `http://localhost:8000/docs` when server is running
- **Database Issues:** Check MongoDB connection and run migrations
- **Import Errors:** Check server logs for detailed error messages
- **Frontend Issues:** Ensure client/venv is properly activated

**Happy scraping! 🕷️➡️📊**
