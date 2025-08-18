# RemotelyX Backend Server

A FastAPI-based backend server for the RemotelyX Job Dashboard, designed to handle job data from n8n scrapers and provide comprehensive analytics and API endpoints.

## 🚀 Features

- **Job Management**: CRUD operations for job postings
- **Advanced Search**: Full-text search with filtering and pagination
- **Real-time Analytics**: Dashboard statistics, skills analysis, and insights
- **MongoDB Integration**: Optimized database with proper indexing
- **n8n Integration**: Ready to receive scraped job data
- **RESTful API**: Clean, documented API endpoints
- **Data Seeding**: Development tools for populating test data

## 🏗️ Architecture

```
server/
├── app/
│   ├── controllers/     # API route handlers
│   ├── services/        # Business logic layer
│   ├── models/          # Data models and schemas
│   ├── core/            # Configuration and database
│   └── utils/           # Utility functions
├── main.py              # FastAPI application entry point
├── start_server.py      # Server startup script
└── requirements.txt     # Python dependencies
```

## 📋 Prerequisites

- Python 3.8+
- MongoDB 4.4+
- pip or poetry

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   cd server
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MongoDB**

   - Ensure MongoDB is running on your system
   - Default connection: `mongodb://localhost:27017`
   - Database will be created automatically: `remotelyx`

4. **Environment Configuration**
   Create a `.env` file in the server directory:
   ```env
   MONGODB_URL=mongodb://localhost:27017
   MONGODB_DB=remotelyx
   SECRET_KEY=your-secret-key-change-in-production
   ```

## 🚀 Running the Server

### Development Mode

```bash
python start_server.py
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### With Environment Variables

```bash
RELOAD=true PORT=8001 python start_server.py
```

## 📊 API Endpoints

### Jobs API (`/api/v1/jobs`)

| Method   | Endpoint                  | Description                            |
| -------- | ------------------------- | -------------------------------------- |
| `GET`    | `/`                       | Get jobs with filtering and pagination |
| `POST`   | `/`                       | Create a new job                       |
| `POST`   | `/bulk`                   | Create multiple jobs                   |
| `GET`    | `/{job_id}`               | Get job by ID                          |
| `PUT`    | `/{job_id}`               | Update job                             |
| `DELETE` | `/{job_id}`               | Delete job                             |
| `GET`    | `/company/{company_name}` | Get jobs by company                    |
| `GET`    | `/recent/{days}`          | Get recent jobs                        |
| `GET`    | `/stats/overview`         | Get job statistics                     |
| `GET`    | `/filters/options`        | Get available filter options           |

### Analytics API (`/api/v1/analytics`)

| Method | Endpoint                  | Description                |
| ------ | ------------------------- | -------------------------- |
| `GET`  | `/dashboard`              | Get dashboard statistics   |
| `GET`  | `/skills/top`             | Get top skills in demand   |
| `GET`  | `/seniority/distribution` | Get seniority distribution |
| `GET`  | `/salary/ranges`          | Get salary ranges by level |
| `GET`  | `/companies/insights`     | Get company insights       |
| `GET`  | `/skills/by-role`         | Get skills mapped to roles |
| `GET`  | `/full`                   | Get complete analytics     |
| `POST` | `/refresh`                | Force refresh analytics    |
| `GET`  | `/overview`               | Get analytics overview     |
| `GET`  | `/trends/weekly`          | Get weekly trends          |

### Seeder API (`/api/v1/seeder`)

| Method   | Endpoint            | Description               |
| -------- | ------------------- | ------------------------- |
| `POST`   | `/seed/sample`      | Seed sample job data      |
| `POST`   | `/seed/n8n`         | Seed jobs from n8n format |
| `POST`   | `/seed/example-n8n` | Seed example n8n data     |
| `DELETE` | `/clear`            | Clear all jobs            |
| `GET`    | `/status`           | Get database status       |

## 🔍 Usage Examples

### 1. Seed Sample Data

```bash
# Seed 50 sample jobs
curl -X POST "http://localhost:8000/api/v1/seeder/seed/sample?count=50"
```

### 2. Get Dashboard Stats

```bash
curl "http://localhost:8000/api/v1/analytics/dashboard"
```

### 3. Search Jobs

```bash
# Search for Python developer jobs
curl "http://localhost:8000/api/v1/jobs/?search=Python&limit=10"
```

### 4. Get Top Skills

```bash
# Get top skills for Developer role
curl "http://localhost:8000/api/v1/analytics/skills/top?role=Developer"
```

### 5. Filter Jobs by Company

```bash
# Get jobs from a specific company
curl "http://localhost:8000/api/v1/jobs/?company=TechCorp&limit=20"
```

## 🗄️ Database Schema

### Jobs Collection

```json
{
  "_id": "ObjectId",
  "data": {
    "company": "string",
    "date_posted": "string",
    "description": "string",
    "employment_type": "string",
    "job_link": "string",
    "location": "string",
    "salary": "string",
    "scraped_at": "string",
    "seniority": "string",
    "soft_skills": ["string"],
    "tech_skills": ["string"],
    "title": "string",
    "updated_at": "string"
  },
  "message": "string",
  "scraped_at": "string",
  "success": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Analytics Collection

```json
{
  "_id": "ObjectId",
  "top_skills": [...],
  "seniority_distribution": {...},
  "salary_ranges_by_level": {...},
  "company_insights": [...],
  "dashboard_stats": {...},
  "calculated_at": "datetime"
}
```

## 🔧 Configuration

### MongoDB Settings

- **URL**: Configured via `MONGODB_URL` environment variable
- **Database**: Configured via `MONGODB_DB` environment variable
- **Indexes**: Automatically created for optimal performance

### API Settings

- **Base Path**: `/api/v1`
- **CORS**: Configured for frontend integration
- **Documentation**: Available at `/docs` (Swagger UI)

## 📈 Performance Features

- **Database Indexing**: Optimized queries with proper MongoDB indexes
- **Text Search**: Full-text search across job titles, descriptions, and skills
- **Pagination**: Efficient pagination for large datasets
- **Caching**: Analytics data caching for improved response times
- **Aggregation**: MongoDB aggregation pipelines for complex analytics

## 🧪 Testing

### Manual Testing

1. Start the server
2. Use the seeder endpoints to populate test data
3. Test API endpoints using the interactive docs at `/docs`

### API Testing

```bash
# Test health endpoint
curl "http://localhost:8000/health"

# Test database connection
curl "http://localhost:8000/api/v1/seeder/status"
```

## 🚀 Deployment

### Docker

```bash
docker build -t remotelyx-backend .
docker run -p 8000:8000 remotelyx-backend
```

### Environment Variables for Production

```env
MONGODB_URL=mongodb://production-mongo:27017
MONGODB_DB=remotelyx_prod
SECRET_KEY=your-production-secret-key
RELOAD=false
```

## 🔗 Frontend Integration

The backend is designed to work seamlessly with the RemotelyX frontend dashboard. Key integration points:

- **CORS**: Configured for frontend domains
- **API Endpoints**: Match frontend data requirements
- **Real-time Data**: Analytics calculated on-demand
- **Search & Filtering**: Comprehensive job search capabilities

## 📝 API Documentation

Interactive API documentation is available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🤝 Contributing

1. Follow the existing code structure
2. Add proper error handling and logging
3. Update API documentation
4. Test with sample data
5. Ensure MongoDB indexes are optimized

## 📞 Support

For backend-related issues:

1. Check the logs for error messages
2. Verify MongoDB connection
3. Test individual endpoints
4. Check API documentation at `/docs`

## 🔮 Future Enhancements

- **Real-time Updates**: WebSocket support for live data
- **Advanced Analytics**: Machine learning insights
- **Job Matching**: AI-powered candidate matching
- **Export Features**: Data export in various formats
- **Monitoring**: Performance metrics and health checks
