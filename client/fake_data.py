# Fake data for RemotelyX Dashboard

# Header data for navbar
header_data = {
    "logo": "Remotely",
    "user": {
        "name": "Racile K.",
        "avatar": "R",
        "notifications": 12
    },
    "theme": "dark",  # or "light"
}

# Sidebar UI data for custom HTML sidebar
sidebar_ui = {
    "date_ranges": [
        {"value": "1-day", "label": "1 day"},
        {"value": "7-days", "label": "1 week", "selected": True},
        {"value": "1-month", "label": "1 month"},
        {"value": "custom", "label": "Custom"},
        {"value": "3-months", "label": "3 months"},
        {"value": "6-months", "label": "6 months"},
        {"value": "1-year", "label": "1 year"},
    ],
    "role_types": [
        "All Roles", "Developer", "Designer", "Product Manager", "DevOps", "Data Scientist"
    ],
    "statuses": [
        {"label": "New", "count": 12, "active": True},
        {"label": "Analyzed", "count": 45, "active": False},
        {"label": "Matched", "count": 88, "active": False},
    ],
    "seniority": [
        {"label": "Junior", "active": False},
        {"label": "Mid", "active": True},
        {"label": "Senior", "active": True},
    ],
    "skills_suggestions": ["React", "Node.js", "Python", "AWS"],
    "companies": [
        "All Companies", "TechCorp Inc.", "StartupXYZ", "Enterprise Solutions", "Analytics Pro", "Creative Studios"
    ],
    "companies_placeholder": "Search company...",
    "salary_ranges": [
        "All Ranges", "$40k - $60k", "$60k - $80k", "$80k - $100k", "$100k+"
    ],
}

# Sidebar filters data
sidebar_filters = {
    "date_range": ["Last 7 days", "Last 30 days", "Last 90 days", "Custom"],
    "job_types": ["Full-time", "Part-time", "Contract", "Freelance"],
    "experience_levels": ["Entry", "Mid-level", "Senior", "Lead", "Executive"],
    "locations": ["Remote", "US", "Europe", "Asia", "Other"],
    "skills": ["Python", "JavaScript", "React", "AWS", "Docker", "Kubernetes", "SQL", "Git"]
}

# Metrics data for stats cards
metrics_data = {
    "active_jobs": 892,
    "new_this_week": 47,
    "avg_process_time": "3.2 days",
    "success_rate": 94.2,
    "total_applications": 1247,
    "interviews_scheduled": 156,
    "offers_sent": 89,
    "hires_made": 67
}

# Top skills data
top_skills = {
    'skill': ['Python', 'JavaScript', 'React', 'AWS', 'Docker', 'Kubernetes', 'SQL', 'Git'],
    'demand_score': [95, 88, 82, 78, 75, 72, 68, 65],
    'seniority': ['Senior', 'Mid-level', 'Senior', 'Senior', 'Mid-level', 'Senior', 'Mid-level', 'Mid-level'],
    'job_count': [156, 142, 128, 98, 87, 76, 134, 89],
    'growth_rate': [12.5, 8.3, 15.2, 22.1, 18.7, 25.4, 9.8, 6.2]
}

# Job listings data
job_listings = [
    {
        "id": "J001",
        "title": "Senior Python Developer",
        "company": "TechCorp Inc.",
        "location": "Remote",
        "type": "Full-time",
        "experience": "Senior",
        "salary": "$120k - $150k",
        "posted_date": "2024-01-15",
        "status": "Active",
        "applications": 24,
        "skills": ["Python", "Django", "AWS", "Docker"]
    },
    {
        "id": "J002",
        "title": "Frontend Engineer",
        "company": "StartupXYZ",
        "location": "San Francisco, CA",
        "type": "Full-time",
        "experience": "Mid-level",
        "salary": "$90k - $110k",
        "posted_date": "2024-01-14",
        "status": "Active",
        "applications": 18,
        "skills": ["React", "JavaScript", "TypeScript", "CSS"]
    },
    {
        "id": "J003",
        "title": "DevOps Specialist",
        "company": "Enterprise Solutions",
        "location": "Remote",
        "type": "Contract",
        "experience": "Senior",
        "salary": "$130k - $160k",
        "posted_date": "2024-01-13",
        "status": "Active",
        "applications": 15,
        "skills": ["Kubernetes", "Docker", "AWS", "Terraform"]
    },
    {
        "id": "J004",
        "title": "Data Scientist",
        "company": "Analytics Pro",
        "location": "New York, NY",
        "type": "Full-time",
        "experience": "Senior",
        "salary": "$140k - $170k",
        "posted_date": "2024-01-12",
        "status": "Active",
        "applications": 31,
        "skills": ["Python", "Machine Learning", "SQL", "Statistics"]
    },
    {
        "id": "J005",
        "title": "UX/UI Designer",
        "company": "Creative Studios",
        "location": "Remote",
        "type": "Full-time",
        "experience": "Mid-level",
        "salary": "$80k - $100k",
        "posted_date": "2024-01-11",
        "status": "Active",
        "applications": 22,
        "skills": ["Figma", "Adobe Creative Suite", "User Research", "Prototyping"]
    }
]

# Trending skills data
trending_skills = [
    {"skill": "AI/ML", "trend": "+45%", "demand": "High"},
    {"skill": "Cybersecurity", "trend": "+38%", "demand": "High"},
    {"skill": "Cloud Computing", "trend": "+32%", "demand": "High"},
    {"skill": "Data Engineering", "trend": "+28%", "demand": "Medium"},
    {"skill": "Blockchain", "trend": "+25%", "demand": "Medium"}
]

# Hard to fill positions
hard_to_fill = [
    {"position": "Senior AI Engineer", "days_open": 45, "applications": 8, "difficulty": "Very High"},
    {"position": "Cybersecurity Specialist", "days_open": 38, "applications": 12, "difficulty": "High"},
    {"position": "DevOps Architect", "days_open": 32, "applications": 15, "difficulty": "High"},
    {"position": "Data Engineer", "days_open": 28, "applications": 18, "difficulty": "Medium"},
    {"position": "Full Stack Developer", "days_open": 25, "applications": 22, "difficulty": "Medium"}
]

# Recent activity data
recent_activity = [
    {"time": "2 min ago", "action": "New job posted", "details": "Senior Python Developer", "type": "job_post"},
    {"time": "15 min ago", "action": "Application received", "details": "Frontend Engineer", "type": "application"},
    {"time": "1 hour ago", "action": "Interview scheduled", "details": "DevOps Specialist", "type": "interview"},
    {"time": "3 hours ago", "action": "Offer sent", "details": "Data Scientist", "type": "offer"},
    {"time": "5 hours ago", "action": "Candidate hired", "details": "UX Designer", "type": "hire"},
    {"time": "1 day ago", "action": "Job closed", "details": "Backend Developer", "type": "job_close"}
]

# Company statistics
company_stats = {
    "total_companies": 156,
    "active_postings": 892,
    "avg_response_time": "2.3 days",
    "candidate_satisfaction": 4.7,
    "time_to_hire": "18.5 days",
    "cost_per_hire": "$4,200"
}

# Geographic distribution
geographic_data = {
    "locations": ["Remote", "US", "Europe", "Asia", "Other"],
    "job_counts": [456, 234, 123, 67, 12],
    "growth_rates": [15.2, 8.7, 12.3, 18.9, 5.4]
}

# Industry breakdown
industry_data = {
    "industries": ["Technology", "Finance", "Healthcare", "E-commerce", "Education", "Other"],
    "job_counts": [567, 234, 123, 89, 67, 45],
    "avg_salary": [125000, 110000, 95000, 105000, 85000, 90000]
}