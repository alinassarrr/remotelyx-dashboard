# 🚀 RemotelyX API - Postman Testing Guide

## Quick Setup

### 1. Import Collection
1. Open Postman
2. Click **"Import"** → **"Upload Files"**  
3. Select: `RemotelyX_API_Updated.postman_collection.json`
4. Click **"Import"**

### 2. Create Environment
1. Click **"Environments"** → **"Create Environment"**
2. Name: `RemotelyX Local`
3. Add these variables:

| Variable | Value |
|----------|--------|
| `base_url` | `http://localhost:8000` |
| `api_base` | `http://localhost:8000/api/v1` |
| `token` | `(leave empty - will be set automatically)` |

## 🔥 **Available API Endpoints**

### **Health & Info**
- ✅ `GET /` - Welcome message
- ✅ `GET /health` - Health check

### **Authentication** 🔐
- ✅ `POST /api/v1/auth/signup` - Register new user
- ✅ `POST /api/v1/auth/login` - Login user  
- ✅ `GET /api/v1/auth/me` - Get current user (requires auth)

### **Jobs** 💼
- ✅ `GET /api/v1/jobs/` - List all jobs
- ✅ `GET /api/v1/jobs/{job_id}` - Get specific job
- ✅ `GET /api/v1/jobs/filters` - Get available filters

### **Analytics** 📊
- ✅ `GET /api/v1/analytics/` - Complete analytics dashboard
- ✅ `GET /api/v1/analytics/kpis` - Key performance indicators
- ✅ `GET /api/v1/analytics/skills` - Skills demand data
- ✅ `GET /api/v1/analytics/seniority` - Seniority distribution  
- ✅ `GET /api/v1/analytics/trending` - Trending skills
- ✅ `GET /api/v1/analytics/hard-to-fill` - Hard to fill roles
- ✅ `GET /api/v1/analytics/recent-activity` - Recent activity

### **Scraped Jobs** 🤖
- ✅ `POST /api/v1/scraped-jobs/import` - Bulk import jobs
- ✅ `POST /api/v1/scraped-jobs/import/single` - Import single job
- ✅ `GET /api/v1/scraped-jobs/stats` - Scraping statistics

## 🧪 **Testing Workflow**

### **Step 1: Test Basic Endpoints**
```
1. GET {{base_url}}/health
2. GET {{base_url}}/
```

### **Step 2: Test Authentication**
```
1. POST {{api_base}}/auth/signup
   Body: {
     "email": "test@example.com",
     "password": "testpass123", 
     "full_name": "Test User"
   }

2. POST {{api_base}}/auth/login
   Body: {
     "email": "test@example.com",
     "password": "testpass123"
   }
   → Save the access_token for next requests
```

### **Step 3: Test Jobs API**
```
1. GET {{api_base}}/jobs/
2. GET {{api_base}}/jobs/?limit=3
3. GET {{api_base}}/jobs/?type=remote
4. GET {{api_base}}/jobs/filters
```

### **Step 4: Test Analytics**
```
1. GET {{api_base}}/analytics/
2. GET {{api_base}}/analytics/kpis
3. GET {{api_base}}/analytics/skills
4. GET {{api_base}}/analytics/seniority
```

## 📝 **Sample Requests**

### **User Registration**
```json
POST /api/v1/auth/signup
{
    "email": "john.doe@example.com",
    "password": "securepass123",
    "full_name": "John Doe"
}
```

### **User Login**
```json
POST /api/v1/auth/login
{
    "email": "john.doe@example.com", 
    "password": "securepass123"
}
```

### **Get Jobs with Filters**
```
GET /api/v1/jobs/?type=remote&limit=5&seniority=senior
```

### **Bulk Import Jobs**
```json
POST /api/v1/scraped-jobs/import
{
    "jobs": [
        {
            "success": true,
            "data": {
                "title": "Senior Python Developer",
                "company": "TechCorp",
                "location": "Remote",
                "type": "remote",
                "seniority": "senior",
                "salary_min": 120000,
                "salary_max": 180000,
                "skills": ["Python", "FastAPI", "MongoDB"],
                "job_link": "https://techcorp.com/jobs/python-dev"
            },
            "message": "Successfully scraped"
        }
    ]
}
```

## 🔑 **Authentication Setup**

### **Auto-Save Token (Postman Script)**
Add this to your login request **Tests** tab:
```javascript
if (pm.response.code === 200) {
    const response = pm.response.json();
    pm.environment.set("token", response.access_token);
}
```

### **Use Token in Headers**
For protected endpoints, add header:
```
Authorization: Bearer {{token}}
```

## ✅ **Expected Responses**

### **Successful Login**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
}
```

### **Jobs List**
```json
[
    {
        "id": "68a0734e1e8ca0b628315f42",
        "title": "Frontend Developer", 
        "company": "WebDesign Pro",
        "location": "Austin",
        "type": "hybrid",
        "seniority": "junior",
        "salary_min": 65000,
        "salary_max": 85000,
        "skills": ["HTML", "CSS", "JavaScript", "React"],
        "status": "new",
        "created_at": "2025-08-16T12:02:22.091000"
    }
]
```

### **Analytics KPIs**
```json
{
    "active_jobs": 5,
    "new_this_week": 0,
    "avg_processing_time": 0.0,
    "success_rate": 0.0,
    "total_jobs": 5
}
```

## 🚨 **Common Issues & Solutions**

### **Server Not Running**
```bash
cd server
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### **CORS Issues**
Make sure your requests include:
```
Content-Type: application/json
```

### **Authentication Errors**
- Check if token is properly set in environment
- Verify token format: `Bearer {{token}}`
- Make sure you're logged in first

## 🎯 **Quick Test Commands**

You can also test with curl:
```bash
# Health check
curl http://localhost:8000/health

# Get jobs
curl http://localhost:8000/api/v1/jobs/

# Login
curl -X POST -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}' \
  http://localhost:8000/api/v1/auth/login

# Get analytics
curl http://localhost:8000/api/v1/analytics/kpis
```

## 🔗 **Useful Links**

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

**Happy Testing! 🚀**
