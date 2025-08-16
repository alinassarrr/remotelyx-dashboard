# RemotelyX Dashboard

A comprehensive job market analytics platform with secure authentication and beautiful data visualizations.

## 🚀 Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd remotelyx-dashboard

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
├── client/                 # Frontend Streamlit Application
│   ├── app.py             # Main application (login + dashboard)
│   ├── requirements.txt   # Python dependencies
│   ├── config.py         # Configuration settings
│   ├── test_dashboard.py # Test suite
│   ├── start_app.sh      # Quick start script (Linux/Mac)
│   ├── run_dashboard.bat # Quick start script (Windows)
│   ├── html/             # Reference HTML designs
│   └── .streamlit/       # Streamlit configuration
├── server/                # Backend (if needed)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

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
```

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
