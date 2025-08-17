# RemotelyX Dashboard

A comprehensive job market analytics platform with AI-powered job scraping, secure authentication, and beautiful data visualizations.

## 🚀 Features

- 📊 **Job Application Tracking** - Track applications, interviews, and outcomes
- 📈 **Analytics Dashboard** - Visualize application success rates and trends
- 🤖 **AI-Powered Job Scraper** - Extract job data using FREE local AI (Ollama)
- 🔐 **User Authentication** - Secure login and user management
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🗄️ **MongoDB Integration** - Robust data storage and management
- ⚡ **Multiple Interfaces** - FastAPI backend, Streamlit dashboard, and REST API

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Frontend   │───▶│   Backend   │───▶│   Ollama    │───▶│  MongoDB    │
│ (Streamlit) │    │  (FastAPI)  │    │ (Local AI)  │    │ (Database)  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- MongoDB (or Docker)
- Ollama (for AI features)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd remotelyx-dashboard
   ```

2. **Start services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **The application will be available at:**
   - Backend API: http://localhost:8000
   - Streamlit Dashboard: http://localhost:8501
   - API Documentation: http://localhost:8000/docs

### Manual Setup

#### 1. Install Ollama (for AI features)
```bash
# Windows
winget install Ollama.Ollama
ollama pull llama3.2
```

#### 2. Install & Start MongoDB
```bash
# Windows
winget install MongoDB.Server
# MongoDB will start automatically
```

#### 3. Backend Setup
```bash
cd server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your configuration
chmod +x run_dev.sh
./run_dev.sh
```

#### 4. Frontend Setup (Streamlit Dashboard)
```bash
cd client
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## 📊 Dashboard Features

### 🔐 Login System
**Demo Accounts:**
- `admin` / `admin123` (Administrator)
- `racile` / `password123` (Manager)
- `demo` / `secret123` (Demo User)
- `user` / `hello123` (Standard User)

### 📱 Dashboard Tabs
1. **Overview** - Key metrics and analytics charts
2. **Job Listings** - Searchable job board with filters
3. **Reports** - Advanced analytics

## 🤖 AI Job Scraper

### What It Extracts
- Job title and company
- Location and employment type
- Salary information
- Seniority level
- Technical skills (Python, React, AWS, etc.)
- Soft skills (Communication, Leadership, etc.)
- Comprehensive job description
- Posting date and job link

### API Endpoints

#### POST /api/v1/scraper/scrape
```json
{
  "job_url": "https://example.com/job-posting"
}
```

#### Response
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
  }
}
```

## 📁 Project Structure

```
remotelyx-dashboard/
├── server/                 # Backend FastAPI Application
│   ├── app/
│   │   ├── controllers/    # API controllers
│   │   │   ├── auth_controller.py
│   │   │   ├── job_controller.py
│   │   │   ├── analytics_controller.py
│   │   │   └── scraper_controller.py
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   │   └── scraper_service.py
│   │   ├── core/          # Core functionality
│   │   │   ├── config.py  # Configuration settings
│   │   │   └── database.py # Database connections
│   │   └── utils/         # Utility functions
│   ├── migrations/        # Database migrations
│   ├── seeds/            # Database seeders
│   └── main.py           # Application entry point
├── client/                # Frontend Streamlit Application
│   ├── app.py             # Main dashboard application
│   ├── requirements.txt   # Python dependencies
│   ├── config.py         # Configuration settings
│   ├── html/             # Reference HTML designs
│   └── .streamlit/       # Streamlit configuration
├── docker-compose.yml     # Docker services
└── README.md             # This file
```

## 🛠️ Development Commands

### Backend (FastAPI)
```bash
cd server
./run_dev.sh              # Start development server
python -m pytest          # Run tests
python manage.py seed      # Seed database
./db.sh reset             # Reset database
```

### Frontend (Streamlit)
```bash
cd client
streamlit run app.py      # Start dashboard
python test_dashboard.py  # Run tests
```

## 📡 API Documentation

Once the backend is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Configuration

### Environment Variables (.env)
```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB=remotelyx

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8501"]

# AI Configuration
OLLAMA_MODEL=llama3.2
```

## 🎨 Design

The dashboard uses a modern dark theme with:
- Purple accent color (`#7174ff`)
- Blue secondary (`#66b9ff`)
- Green success (`#66fe90`)
- Professional gradients and animations

## 🛡️ Error Handling & Features

- **AI fallback**: If AI extraction fails, uses regex-based fallback
- **Validation**: Input validation for URLs and data
- **Logging**: Comprehensive logging for debugging
- **Graceful degradation**: Continues working even if components fail
- **Deduplication**: Automatic job data deduplication
- **Security**: SHA-256 password hashing and secure authentication

## 🎯 Why This Platform?

- **No API costs** - Uses free local AI (Ollama)
- **No hardcoded selectors** - AI adapts to any website structure
- **Future-proof** - Works with new job sites without code changes
- **Privacy-focused** - All processing happens locally
- **Comprehensive** - Full dashboard + scraping + analytics in one platform

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the [Issues](../../issues) page
2. Create a new issue with detailed information
3. Include logs and error messages when possible

---

**Built with ❤️ | Secure • Fast • Beautiful • AI-Powered**