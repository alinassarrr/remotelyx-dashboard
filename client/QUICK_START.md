# 🚀 Quick Start Guide

## Get the Dashboard Running in 3 Steps!

### 1. **Install Dependencies** (One-time setup)

```bash
# Navigate to client directory
cd client

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 2. **Run the Dashboard**

```bash
# Make sure you're in the client directory with venv activated
source venv/bin/activate

# Start the dashboard
streamlit run app.py
```

### 3. **Open in Browser**

- The dashboard will automatically open at: `http://localhost:8501`
- If it doesn't open automatically, manually navigate to that URL

---

## 🎯 What You'll See

The dashboard includes all the features from your design:

✅ **Overview Tab:**

- 4 key metric cards (Active Jobs, New This Week, Avg Processing, Success Rate)
- Skills in Demand horizontal bar chart
- Seniority Distribution donut chart
- Salary ranges by experience level
- Trending Skills with percentage changes

✅ **Job Listings Tab (NEW!):**

- 156 job listings with realistic data
- Interactive job cards with status badges (NEW, ANALYZED, MATCHED)
- Advanced filtering by status, seniority, skills, company, and salary
- Search functionality for job titles, companies, and skills
- Card View and Table View modes
- Action buttons (Save, Analyze, Details) for each job

✅ **Left Sidebar Filters:**

- **Overview Tab:** Date range, role type, seniority, skills, and company filters
- **Job Listings Tab:** Enhanced filters including job status, salary range, and more
- Real-time filtering with apply/clear functionality

✅ **Interactive Features:**

- Real-time filtering and search
- Responsive design
- Session state persistence
- Professional dark theme UI
- Hover effects and smooth transitions

---

## 🆕 **Job Listings Features**

The new Job Listings tab provides a comprehensive job management interface:

### **Job Cards Include:**

- Job title and company name
- Location, time posted, and seniority level
- Required skills as clickable tags
- Salary range in green
- Status badge (NEW/ANALYZED/MATCHED)
- Action buttons for job management

### **Advanced Filtering:**

- **Status:** New (12), Analyzed (45), Matched (88)
- **Seniority:** Junior, Mid, Senior
- **Skills:** Add/remove skills dynamically
- **Company:** Filter by specific companies
- **Salary Range:** All ranges, $40k-$60k, $60k-$80k, $80k-$100k, $100k+

### **View Modes:**

- **Card View:** Beautiful job cards in a grid layout
- **Table View:** Compact table format for quick scanning

### **Search & Sort:**

- Quick search across job titles, companies, and skills
- Sort by newest first, salary, company name, etc.

---

## 🛠️ Alternative Launch Methods

### Option 1: Use the Shell Script (Linux/Mac)

```bash
chmod +x run_dashboard.sh
./run_dashboard.sh
```

### Option 2: Use the Batch File (Windows)

```bash
run_dashboard.bat
```

### Option 3: Manual Launch

```bash
source venv/bin/activate
streamlit run app.py
```

---

## 🔧 Troubleshooting

**If you get permission errors:**

```bash
chmod +x run_dashboard.sh
```

**If dependencies fail to install:**

```bash
# Make sure you have python3-venv installed
sudo apt install python3.12-venv
```

**If the dashboard doesn't start:**

```bash
# Check if port 8501 is available
lsof -i :8501
# Kill any process using that port if needed
kill -9 <PID>
```

---

## 📱 Dashboard Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Data refreshes automatically
- **Interactive Charts**: Hover over charts for detailed information
- **Professional UI**: Dark theme with modern design
- **Filter Persistence**: Your filter selections are remembered
- **Job Management**: Complete job listing and filtering system

---

## 🎨 Customization

Want to modify the dashboard? Check out:

- `config.py` - Configuration settings
- `app.py` - Main dashboard code
- CSS styling in the app.py file
- Job data generation in the `generate_job_listings()` function

---

## 🆘 Need Help?

Run the test suite to verify everything works:

```bash
source venv/bin/activate
python test_dashboard.py
```

This will check all components including the new job listings functionality!

---

## 🚀 **Ready to Explore?**

1. **Start with Overview Tab**: See your key metrics and analytics
2. **Switch to Job Listings**: Explore the comprehensive job management system
3. **Try the Filters**: Experiment with different filter combinations
4. **Switch View Modes**: Compare Card View vs Table View
5. **Search Jobs**: Use the search bar to find specific opportunities

The dashboard is now a complete job market analytics and management platform! 🎉
