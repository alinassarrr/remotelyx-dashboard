# 🧪 RemotelyX Dashboard API Testing with Postman

This guide shows you how to test all the RemotelyX Dashboard APIs using Postman with the provided collection.

## 📋 Prerequisites

Before starting, make sure you have:

1. **Postman installed** - [Download here](https://www.postman.com/downloads/)
2. **Backend server running** on `http://localhost:8000`
3. **MongoDB and Redis running** (for data persistence)

## 🚀 Quick Setup

### 1. Import the Postman Collection

1. **Download the collection file**: `RemotelyX_API.postman_collection.json`
2. **Open Postman**
3. **Click "Import"** button (top left)
4. **Drag & drop** the JSON file or click "Choose Files"
5. **Click "Import"** to add the collection

### 2. Set Environment Variables

The collection uses variables for easy testing. Set these in Postman:

| Variable       | Default Value           | Description                  |
| -------------- | ----------------------- | ---------------------------- |
| `base_url`     | `http://localhost:8000` | API base URL                 |
| `access_token` | _(auto-set)_            | JWT token for authentication |
| `user_id`      | _(auto-set)_            | Current user ID              |
| `job_id`       | _(auto-set)_            | Job ID for testing           |

**To set variables:**

1. Click the **"Environment"** tab
2. Create **"New Environment"** called "RemotelyX Local"
3. Add the `base_url` variable with value `http://localhost:8000`
4. **Save** and **Select** this environment

## 🔄 Testing Workflow

### Step 1: Health Check

Start by testing the health endpoint to ensure your API is running:

```http
GET {{base_url}}/health
```

**Expected Response:**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "version": "1.0.0"
}
```

### Step 2: User Registration

Create a new user account:

```http
POST {{base_url}}/api/v1/auth/register
Content-Type: application/json

{
  "email": "test@remotelyx.com",
  "password": "SecurePassword123!",
  "full_name": "Test User",
  "phone": "+1234567890"
}
```

**Expected Response:**

```json
{
  "id": "user_id_here",
  "email": "test@remotelyx.com",
  "full_name": "Test User",
  "phone": "+1234567890",
  "is_active": true,
  "created_at": "2024-01-01T12:00:00Z"
}
```

### Step 3: User Login

Authenticate and get access token:

```http
POST {{base_url}}/api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=test@remotelyx.com
password=SecurePassword123!
```

**Expected Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

> 💡 **Note:** The access token is automatically stored in the `access_token` variable for subsequent requests.

### Step 4: Test Authenticated Endpoints

Now you can test all protected endpoints. The collection automatically includes the Bearer token.

## 📊 API Endpoints Overview

### 🔐 Authentication Endpoints

| Method | Endpoint                | Description       | Auth Required |
| ------ | ----------------------- | ----------------- | ------------- |
| `POST` | `/api/v1/auth/register` | Register new user | ❌            |
| `POST` | `/api/v1/auth/login`    | Login user        | ❌            |
| `GET`  | `/api/v1/auth/me`       | Get current user  | ✅            |

### 💼 Job Management Endpoints

| Method   | Endpoint              | Description    | Auth Required |
| -------- | --------------------- | -------------- | ------------- |
| `POST`   | `/api/v1/jobs`        | Create new job | ✅            |
| `GET`    | `/api/v1/jobs`        | Get all jobs   | ✅            |
| `GET`    | `/api/v1/jobs/{id}`   | Get job by ID  | ✅            |
| `PUT`    | `/api/v1/jobs/{id}`   | Update job     | ✅            |
| `DELETE` | `/api/v1/jobs/{id}`   | Delete job     | ✅            |
| `GET`    | `/api/v1/jobs/search` | Search jobs    | ✅            |

### 📈 Analytics Endpoints

| Method | Endpoint                      | Description              | Auth Required |
| ------ | ----------------------------- | ------------------------ | ------------- |
| `GET`  | `/api/v1/analytics/dashboard` | Get dashboard stats      | ✅            |
| `GET`  | `/api/v1/analytics/timeline`  | Get application timeline | ✅            |
| `GET`  | `/api/v1/analytics/skills`    | Get skills analysis      | ✅            |

## 🧪 Detailed Test Cases

### Job Creation Test

```http
POST {{base_url}}/api/v1/jobs
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "title": "Senior Full-Stack Developer",
  "company": "TechCorp Inc.",
  "location": "Remote",
  "job_type": "FULL_TIME",
  "remote_type": "FULLY_REMOTE",
  "salary_min": 80000,
  "salary_max": 120000,
  "description": "We are looking for an experienced full-stack developer.",
  "requirements": ["React", "Node.js", "TypeScript", "MongoDB"],
  "url": "https://techcorp.com/careers/senior-fullstack",
  "status": "APPLIED"
}
```

### Job Search Test

```http
GET {{base_url}}/api/v1/jobs/search?q=developer&company=TechCorp&status=APPLIED
Authorization: Bearer {{access_token}}
```

### Analytics Dashboard Test

```http
GET {{base_url}}/api/v1/analytics/dashboard
Authorization: Bearer {{access_token}}
```

**Expected Response:**

```json
{
  "total_jobs": 25,
  "applications_this_week": 5,
  "response_rate": 0.24,
  "avg_response_time": 7.5,
  "status_distribution": {
    "APPLIED": 10,
    "INTERVIEW": 3,
    "OFFER": 1,
    "REJECTED": 8,
    "WITHDRAWN": 3
  }
}
```

## 🔧 Advanced Testing Features

### Automated Testing Scripts

The collection includes **automated test scripts** that:

✅ **Validate response status codes**  
✅ **Check response structure**  
✅ **Store variables automatically**  
✅ **Verify data integrity**

### Pre-request Scripts

**Auto-set base URL** if not configured:

```javascript
if (!pm.variables.get("base_url")) {
  pm.variables.set("base_url", "http://localhost:8000");
}
```

### Response Tests

**Example authentication test:**

```javascript
pm.test("Response contains access token", function () {
  const responseJson = pm.response.json();
  pm.expect(responseJson).to.have.property("access_token");
  pm.expect(responseJson.token_type).to.eql("bearer");

  // Store for future requests
  pm.variables.set("access_token", responseJson.access_token);
});
```

## 🚀 Running Tests

### Individual Request Testing

1. **Select a request** from the collection
2. **Click "Send"**
3. **Check response** in the bottom panel
4. **View test results** in the "Test Results" tab

### Collection Runner (Automated)

1. **Click "Run Collection"** (top right)
2. **Select environment** (RemotelyX Local)
3. **Choose requests** to run
4. **Click "Start Run"**
5. **View detailed results**

## 🔍 Troubleshooting

### Common Issues

**❌ 401 Unauthorized**

- **Solution**: Make sure you've logged in and the `access_token` is set
- **Check**: Environment variables are selected

**❌ 404 Not Found**

- **Solution**: Verify the backend server is running on `http://localhost:8000`
- **Check**: API endpoints match your backend routes

**❌ 500 Internal Server Error**

- **Solution**: Check backend logs for database connection issues
- **Check**: MongoDB and Redis are running

**❌ Connection Error**

- **Solution**: Ensure backend server is running
- **Check**: `base_url` variable is correct

### Debugging Tips

1. **Check Console Logs**: View Postman console for detailed request/response data
2. **Verify Environment**: Ensure correct environment is selected
3. **Check Variables**: View current variable values in environment
4. **Test Order**: Run requests in the correct sequence (Register → Login → Other APIs)

## 📱 Alternative Testing Methods

### Using cURL

```bash
# Health Check
curl -X GET http://localhost:8000/health

# Register User
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","full_name":"Test User"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123"
```

### Using the Test Script

Run the included test script:

```bash
chmod +x test_api.sh
./test_api.sh
```

## 📊 Test Data Examples

### Sample Job Data

```json
{
  "title": "Frontend Developer",
  "company": "StartupXYZ",
  "location": "San Francisco, CA",
  "job_type": "FULL_TIME",
  "remote_type": "HYBRID",
  "salary_min": 70000,
  "salary_max": 95000,
  "description": "Join our team building the next-gen platform.",
  "requirements": ["React", "JavaScript", "CSS", "Git"],
  "url": "https://startupxyz.com/careers/frontend",
  "status": "WISHLIST"
}
```

### Expected Response Formats

**Job Creation Response:**

```json
{
  "id": "64f123456789012345678901",
  "title": "Frontend Developer",
  "company": "StartupXYZ",
  "user_id": "64f123456789012345678900",
  "status": "WISHLIST",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

---

## 🎯 Testing Checklist

Before considering your API fully tested, ensure:

- [ ] **Health check** returns 200
- [ ] **User registration** works with valid data
- [ ] **User login** returns valid JWT token
- [ ] **Protected endpoints** require authentication
- [ ] **Job CRUD operations** work correctly
- [ ] **Search functionality** returns filtered results
- [ ] **Analytics endpoints** return proper data structure
- [ ] **Error responses** return appropriate status codes
- [ ] **Data validation** rejects invalid input
- [ ] **Pagination** works for large datasets

**Happy Testing! 🚀**
