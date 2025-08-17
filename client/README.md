# RemotelyX Dashboard

A comprehensive job market analytics dashboard built with Streamlit, featuring **secure authentication**, real-time data visualization, and interactive filtering capabilities.

## ✨ Features

### 🔐 **Authentication System**

- **Beautiful Login Page** with matching design aesthetic
- **Demo Accounts** for quick testing
- **Secure Password Hashing** (SHA-256)
- **Session Management** with automatic logout
- **User Profile Display** in dashboard header

### 📊 **Dashboard Features**

- **Dark Theme UI**: Modern, professional dashboard interface
- **Interactive Filters**: Date range, role type, seniority, skills, and company filters
- **Key Metrics**: Active jobs, new jobs, processing time, and success rate
- **Skills Analysis**: Top skills in demand with horizontal bar charts
- **Seniority Distribution**: Donut chart showing job distribution by experience level
- **Trending Skills**: Real-time trending skills with percentage changes
- **Job Listings**: Complete job board with 156+ realistic job postings
- **Responsive Design**: Optimized for different screen sizes

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd client
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the Application

```bash
# Method 1: Direct start
streamlit run login.py

# Method 2: Use launcher script
chmod +x run_dashboard.sh
./run_dashboard.sh

# Method 3: Windows
run_dashboard.bat
```

### 3. Login to Dashboard

- **URL**: Open `http://localhost:8501`
- **Login Page**: Will appear first
- **Demo Accounts**: Click any demo account button for instant access

## 👤 Demo Accounts

| Username | Password      | Role          | Description                 |
| -------- | ------------- | ------------- | --------------------------- |
| `admin`  | `admin123`    | Administrator | Full access to all features |
| `racile` | `password123` | Manager       | Manager-level access        |
| `demo`   | `secret123`   | Demo User     | Standard demo account       |
| `user`   | `hello123`    | Standard User | Basic user access           |

## 🎯 Application Flow

1. **Login Page** (`login.py`) - First screen with authentication
2. **Dashboard** (`app.py`) - Main application (requires authentication)
3. **Logout** - Clears session and returns to login

## 📁 Project Structure

```
client/
├── login.py              # Login page with authentication
├── app.py                # Main dashboard application
├── requirements.txt      # Python dependencies
├── config.py            # Configuration settings
├── test_dashboard.py    # Test suite
├── .streamlit/
│   └── config.toml      # Streamlit configuration
├── run_dashboard.sh     # Linux/Mac launcher
├── run_dashboard.bat    # Windows launcher
└── README.md           # Documentation
```

## 🔧 Technical Details

### Authentication

- **Password Hashing**: SHA-256 for secure password storage
- **Session State**: Streamlit session management for user state
- **Auto-redirect**: Unauthorized users redirected to login
- **Logout Functionality**: Clean session termination

### Data Generation

- **Cached Functions**: `@st.cache_data` for optimal performance
- **Realistic Data**: 156 job listings with complete metadata
- **Dynamic Charts**: Interactive Plotly visualizations
- **Real-time Updates**: Data refreshes every 2 minutes

### Design System

- **Color Palette**: Matches HTML design exactly
  - Purple: `#7174ff` (primary)
  - Blue: `#66b9ff` (secondary)
  - Green: `#66fe90` (success)
  - Dark: `#111417` (background)
- **CSS Variables**: Consistent theming throughout
- **Responsive Layout**: Works on all screen sizes

## 🛠️ Development

### Running Tests

```bash
source venv/bin/activate
python test_dashboard.py
```

### Adding New Users

Edit the `USERS` dictionary in `login.py`:

```python
USERS = {
    "username": "hashed_password_sha256",
    # Add more users...
}
```

### Customization

- **Colors**: Modify CSS variables in both files
- **Data**: Update `generate_sample_data()` function
- **UI**: Adjust HTML/CSS in markdown sections

## 🚀 Deployment

### Local Development

```bash
streamlit run login.py --server.port 8501
```

### Production Deployment

1. **Streamlit Cloud**: Push to GitHub and deploy
2. **Docker**: Create container with requirements
3. **Heroku**: Deploy with Procfile
4. **AWS/GCP**: Use cloud hosting services

### Environment Variables

For production, consider using environment variables:

```bash
export STREAMLIT_LOGIN_USERS='{"admin":"hash1","user":"hash2"}'
```

## 📊 Features Deep Dive

### Login System

- **Secure**: Password hashing prevents plain-text storage
- **User-Friendly**: Demo accounts for easy testing
- **Responsive**: Mobile-friendly design
- **Fast**: Instant login with demo accounts

### Dashboard Analytics

- **Overview Tab**: Key metrics and charts
- **Job Listings**: Searchable job board
- **Reports**: Coming soon placeholder
- **Real-time**: Live data updates

### Data Visualization

- **Skills Chart**: Horizontal bar chart with demand levels
- **Seniority Chart**: Donut chart with distribution
- **Trending Skills**: Live percentage changes
- **Interactive**: Hover effects and animations

## 🎨 Design Philosophy

The dashboard follows a **dark-first design** approach with:

- **Professional Aesthetic**: Clean, modern interface
- **Consistent Branding**: Purple/blue/green color scheme
- **Intuitive Navigation**: Clear hierarchy and flow
- **Accessibility**: High contrast and readable fonts

## 📞 Support

- **Issues**: Check console for error messages
- **Performance**: Restart if data seems stale
- **Authentication**: Use demo accounts for testing
- **Browser**: Works best in Chrome/Firefox/Safari

---

**Built with ❤️ using Streamlit | Secure • Fast • Beautiful**
