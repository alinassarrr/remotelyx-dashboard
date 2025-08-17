# RemotelyX Dashboard

A comprehensive job market analytics platform with secure authentication and beautiful data visualizations.

## 🚀 Quick Start

````bash
# Clone the repository
git clone <your-repo-url>
# RemotelyX Dashboard

A comprehensive job application tracking dashboard for remote job seekers.

## Features

- 📊 **Job Application Tracking** - Track applications, interviews, and outcomes
- 📈 **Analytics Dashboard** - Visualize application success rates and trends
- 🔐 **User Authentication** - Secure login and user management
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🚀 **Modern Tech Stack** - FastAPI backend with MongoDB, React frontend

## Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for APIs
- **MongoDB** - NoSQL database with Beanie ODM
- **Redis** - Caching and session storage
- **Python 3.11+** - Latest Python version

### Frontend
- **React** - Modern JavaScript library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool and dev server

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB (or Docker)
- Redis (or Docker)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd remotelyx-dashboard
````

2. **Start services with Docker Compose**

   ```bash
   docker-compose up -d
   ```

3. **The application will be available at:**
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:3000
   - MongoDB: localhost:27017
   - Redis: localhost:6379

### Manual Setup

#### Backend Setup

1. **Navigate to server directory**

   ```bash
   cd server
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database setup**

   ```bash
   chmod +x db.sh
   ./db.sh
   ```

6. **Start the development server**
   ```bash
   chmod +x run_dev.sh
   ./run_dev.sh
   ```

#### Frontend Setup

1. **Navigate to client directory**

   ```bash
   cd client
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

## API Documentation

Once the backend is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
remotelyx-dashboard/
├── server/                 # Backend API
│   ├── app/
│   │   ├── controllers/    # API controllers
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── utils/         # Utility functions
│   ├── migrations/        # Database migrations
│   ├── seeds/            # Database seeders
│   ├── tests/            # Backend tests
│   └── main.py           # Application entry point
├── client/                # Frontend application
├── docker-compose.yml     # Docker services
└── README.md
```

## Development Commands

### Backend

```bash
# Run development server
./run_dev.sh

# Run tests
python -m pytest

# Seed database
python manage.py seed

# Reset database
./db.sh reset
```

### Frontend

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test
```

## API Testing

Use the included Postman collection:

```bash
# Import RemotelyX_API.postman_collection.json into Postman
# Or run tests via command line:
./test_api.sh
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## Environment Variables

### Backend (.env)

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=remotelyx_dashboard

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) page
2. Create a new issue with detailed information
3. Include logs and error messages when possible

---

**Happy job hunting! 🚀**

# Navigate to client directory

cd client

# Setup virtual environment

python3 -m venv venv
source venv/bin/activate

# Install dependencies

pip install -r requirements.txt

# Start the application

streamlit run app.py

```

## 📁 Project Structure

```

remotelyx-dashboard/
├── client/ # Frontend Streamlit Application
│ ├── app.py # Main application (login + dashboard)
│ ├── requirements.txt # Python dependencies
│ ├── config.py # Configuration settings
│ ├── test_dashboard.py # Test suite
│ ├── start_app.sh # Quick start script (Linux/Mac)
│ ├── run_dashboard.bat # Quick start script (Windows)
│ ├── html/ # Reference HTML designs
│ └── .streamlit/ # Streamlit configuration
├── server/ # Backend (if needed)
├── .gitignore # Git ignore rules
└── README.md # This file

````

## 🔐 Login System

The application includes a secure authentication system:

**Demo Accounts:**

- `admin` / `admin123` (Administrator)
- `racile` / `password123` (Manager)
- `demo` / `secret123` (Demo User)
- `user` / `hello123` (Standard User)

## 🎯 Features

- **Secure Authentication** with SHA-256 password hashing
- **Beautiful Login Page** matching dashboard design
- **Interactive Dashboard** with real-time analytics
- **Job Listings Board** with 156+ sample jobs
- **Skills Analysis** with demand charts
- **Responsive Design** for all devices

## 🛠️ Development

### Running Tests

```bash
cd client
source venv/bin/activate
python test_dashboard.py
````

### Adding New Features

1. Make changes to `client/app.py`
2. Test locally with `streamlit run app.py`
3. Run test suite to ensure stability
4. Commit and push changes

## 📊 Dashboard Tabs

1. **Overview** - Key metrics and analytics charts
2. **Job Listings** - Searchable job board with filters
3. **Reports** - Advanced analytics (coming soon)

## 🎨 Design

The dashboard uses a modern dark theme with:

- Purple accent color (`#7174ff`)
- Blue secondary (`#66b9ff`)
- Green success (`#66fe90`)
- Professional gradients and animations

## 🔧 Configuration

- **Port**: Default 8501 (configurable in `.streamlit/config.toml`)
- **Theme**: Dark mode with custom CSS
- **Data**: Generated sample data (156 jobs, 9 skills)

## 📱 Access

Once running, visit: `http://localhost:8501`

---

**Built with ❤️ using Streamlit | Secure • Fast • Beautiful**

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
