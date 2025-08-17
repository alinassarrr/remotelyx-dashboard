# RemotelyX Server - Backend API

This is the backend server for RemotelyX, providing job market analytics and insights for recruiters.

## 🚀 Quick Start

### Using Poetry (Recommended)

1. **Navigate to server directory**:

   ```bash
   cd server
   ```

2. **Install dependencies**:

   ```bash
   poetry install
   poetry shell
   ```

3. **Start MongoDB**:

   ```bash
   docker run -d -p 27017:27017 --name mongo mongo:latest
   ```

4. **Run the API**:
   ```bash
   poetry run uvicorn main:app --reload
   ```

### Using pip

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API**:
   ```bash
   uvicorn main:app --reload
   ```

## 📚 API Documentation

Once running, access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 API Endpoints

- **Base URL**: http://localhost:8000
- **API Version**: /api/v1

### Authentication

- `POST /api/v1/auth/signup` - Create user account
- `POST /api/v1/auth/login` - Authenticate user
- `GET /api/v1/auth/me` - Get current user info

### Jobs

- `GET /api/v1/jobs` - List jobs with filtering
- `POST /api/v1/jobs` - Create new job
- `GET /api/v1/jobs/{id}` - Get specific job
- `PUT /api/v1/jobs/{id}` - Update job
- `DELETE /api/v1/jobs/{id}` - Delete job

### Analytics

- `GET /api/v1/analytics` - Complete analytics data
- `GET /api/v1/analytics/kpis` - Key performance indicators
- `GET /api/v1/analytics/skills` - Skills demand analysis
- `GET /api/v1/analytics/seniority` - Seniority distribution
- `GET /api/v1/analytics/trending` - Trending skills
- `GET /api/v1/analytics/hard-to-fill` - Hard-to-fill roles
- `GET /api/v1/analytics/recent-activity` - Recent activity logs

## 🏗 Project Structure

```
server/
├── main.py                 # FastAPI entrypoint
├── app/                    # Application package
│   ├── core/              # Core utilities (config, security, database)
│   ├── models/            # MongoDB data models
│   ├── schemas/           # Pydantic validation schemas
│   ├── services/          # Business logic layer
│   ├── controllers/       # API route handlers
│   ├── utils/             # Shared utilities
│   └── tests/             # Test suite
├── migrations/             # Database migrations
│   ├── migration_manager.py # Migration system
│   └── __init__.py
├── seeds/                  # Database seeding
│   ├── seed_manager.py    # Seeding system
│   └── __init__.py
├── manage.py               # Database management script
├── db.sh                   # Database management shell script
├── run_dev.sh              # Development startup script
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Poetry configuration
├── README.md               # This file
└── MIGRATIONS_README.md    # Detailed migration guide
```

## 🧪 Testing

```bash
# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app
```

## 🔧 Configuration

Environment variables (can be set in `.env` file):

```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB=remotelyx
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
