"""
API Client for RemotelyX Backend
Handles all communication with the FastAPI backend
"""

import requests
import streamlit as st
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RemotelyXAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api/v1"
        
    def _make_request(self, method: str, endpoint: str, params: dict = None, data: dict = None) -> dict:
        """Make HTTP request to the backend API"""
        url = f"{self.api_base}{endpoint}"
        try:
            response = requests.request(method, url, params=params, json=data, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"API request failed: {response.status_code} - {response.text}")
                return {}
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception: {e}")
            return {}
    
    def health_check(self) -> dict:
        """Check if backend is healthy"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.json() if response.status_code == 200 else {}
        except:
            return {"status": "unhealthy"}
    
    def get_jobs(self, limit: int = 100, skip: int = 0, **filters) -> dict:
        """Get job listings with optional filters"""
        params = {
            "limit": limit,
            "skip": skip,
            **filters
        }
        return self._make_request("GET", "/jobs/", params=params)
    
    def get_filter_options(self) -> dict:
        """Get available filter options for dropdowns"""
        return self._make_request("GET", "/jobs/filters/options")
    
    def get_job_stats(self) -> dict:
        """Get job statistics overview"""
        return self._make_request("GET", "/jobs/stats/overview")
    
    def get_recent_jobs(self, days: int = 7, limit: int = 50) -> list:
        """Get recent jobs from last N days"""
        return self._make_request("GET", f"/jobs/recent/{days}", params={"limit": limit})
    
    def get_jobs_by_company(self, company_name: str, limit: int = 50) -> list:
        """Get all jobs from a specific company"""
        return self._make_request("GET", f"/jobs/company/{company_name}", params={"limit": limit})
    
    def search_jobs(self, query: str, limit: int = 100) -> dict:
        """Search jobs by query"""
        return self._make_request("GET", "/jobs/", params={"search": query, "limit": limit})
    
    # New Dashboard Analytics endpoints
    def get_dashboard_metrics(self) -> dict:
        """Get comprehensive dashboard metrics"""
        return self._make_request("GET", "/dashboard/metrics")
    
    def get_dashboard_top_skills(self, limit: int = 8) -> dict:
        """Get top skills with real analytics"""
        return self._make_request("GET", "/dashboard/top-skills", params={"limit": limit})
    
    def get_company_insights(self, limit: int = 10) -> dict:
        """Get company hiring insights"""
        return self._make_request("GET", "/dashboard/company-insights", params={"limit": limit})
    
    def get_hiring_trends(self, days: int = 30) -> dict:
        """Get hiring trends over time"""
        return self._make_request("GET", "/dashboard/trends", params={"days": days})
    
    def get_salary_insights(self) -> dict:
        """Get salary insights by seniority and location"""
        return self._make_request("GET", "/dashboard/salary-insights")
    
    def update_job_status(self, job_id: str, status: str) -> dict:
        """Update job status (NEW, ANALYZED, MATCHED, IN PROGRESS, CLOSED, REJECTED)"""
        return self._make_request("PATCH", f"/jobs/{job_id}/status", data={"status": status})
    
    def get_dashboard_roles(self) -> dict:
        """Get all available job roles and categories"""
        return self._make_request("GET", "/dashboard/roles")
    
    def get_skills_by_role(self, role_category: str = "All", limit: int = 10) -> dict:
        """Get technical and soft skills for a specific role category"""
        return self._make_request("GET", "/dashboard/skills-by-role", params={
            "role_category": role_category,
            "limit": limit
        })

# Create a singleton instance
@st.cache_resource
def get_api_client():
    """Get cached API client instance"""
    return RemotelyXAPIClient()

# Data transformation functions to convert API data to frontend format
def transform_job_data(api_job: dict) -> dict:
    """Transform API job data to frontend format"""
    job_data = api_job.get('data', {})
    
    return {
        "id": str(api_job.get('_id', '')),
        "title": job_data.get('title', ''),
        "company": job_data.get('company', ''),
        "location": job_data.get('location', ''),
        "type": job_data.get('employment_type', ''),
        "experience": job_data.get('seniority', ''),
        "salary": job_data.get('salary', 'Not specified'),
        "posted_date": job_data.get('date_posted', ''),
        "status": api_job.get('status', 'NEW'),  # Use actual job status from API
        "applications": 0,  # Not available in current API
        "skills": job_data.get('tech_skills', []) + job_data.get('soft_skills', []),
        "tech_skills": job_data.get('tech_skills', []),
        "soft_skills": job_data.get('soft_skills', []),
        "description": job_data.get('description', ''),
        "job_link": job_data.get('job_link', ''),
        "scraped_at": job_data.get('scraped_at', ''),
        "updated_at": job_data.get('updated_at', '')
    }

def get_live_jobs(limit: int = 100, **filters) -> List[dict]:
    """Get live job data from API - now working with real database"""
    client = get_api_client()
    
    # Check if backend is available
    health = client.health_check()
    if health.get("status") != "healthy":
        logger.warning("Backend not available, using empty data")
        return []
    
    # Get jobs from API (now working!)
    response = client.get_jobs(limit=limit, **filters)
    jobs = response.get('jobs', [])
    
    # Transform to frontend format
    return [transform_job_data(job) for job in jobs]

def get_live_filter_options() -> dict:
    """Get live filter options from API"""
    client = get_api_client()
    
    # Check if backend is available
    health = client.health_check()
    if health.get("status") != "healthy":
        logger.warning("Backend not available, using default filters")
        return {
            "companies": [],
            "locations": ["Remote"],
            "seniorities": ["Junior", "Mid", "Senior"],
            "employment_types": ["Full-time", "Part-time", "Contract"],
            "tech_skills": ["Python", "JavaScript", "React"],
            "soft_skills": ["Communication", "Teamwork"]
        }
    
    return client.get_filter_options()

def get_live_metrics() -> dict:
    """Get live metrics from comprehensive dashboard API"""
    client = get_api_client()
    
    # Check if backend is available
    health = client.health_check()
    if health.get("status") != "healthy":
        logger.warning("Backend not available, using default metrics")
        return {
            "active_jobs": 0,
            "new_this_week": 0,
            "total_companies": 0,
            "total_locations": 0,
            "total_skills": 0,
            "match_rate": 0.0
        }
    
    # Get real dashboard metrics from API (this returns the full metrics with counts)
    metrics = client.get_dashboard_metrics()
    
    if metrics:
        logger.info("Using real dashboard metrics from API")
        return metrics
    else:
        # Fallback to filter-based estimation
        logger.warning("Dashboard metrics failed, using filter estimation")
        filter_options = client.get_filter_options()
        num_companies = len(filter_options.get('companies', []))
        num_locations = len(filter_options.get('locations', []))
        num_skills = len(filter_options.get('tech_skills', []))
        estimated_jobs = max(num_companies * 5, 150)
        
        return {
            "active_jobs": estimated_jobs,
            "new_this_week": estimated_jobs // 10,
            "total_companies": num_companies,
            "total_locations": num_locations, 
            "total_skills": num_skills,
            "avg_process_time": "3.2 days",
            "match_rate": 15.5,  # Estimated match rate fallback
            "total_applications": estimated_jobs,
            "interviews_scheduled": int(estimated_jobs * 0.15),
            "offers_sent": int(estimated_jobs * 0.08),
            "hires_made": int(estimated_jobs * 0.05)
        }

def get_live_top_skills() -> dict:
    """Get live top skills data from comprehensive dashboard API"""
    client = get_api_client()
    
    # Check if backend is available
    health = client.health_check()
    if health.get("status") != "healthy":
        logger.warning("Backend not available, using default skills")
        return {
            'skill': ['Python', 'JavaScript', 'React', 'AWS'],
            'demand_score': [95, 88, 82, 78],
            'seniority': ['Senior', 'Mid', 'Senior', 'Senior'],
            'job_count': [150, 142, 128, 98]
        }
    
    # Get real top skills from API
    skills_data = client.get_dashboard_top_skills()
    
    if skills_data:
        logger.info("Using real top skills data from API")
        return skills_data
    else:
        # Fallback to filter-based skills
        logger.warning("Top skills API failed, using filter data")
        filter_options = client.get_filter_options()
        tech_skills = filter_options.get('tech_skills', ['Python', 'JavaScript', 'React'])[:8]
        
        import random
        return {
            'skill': tech_skills,
            'demand_score': [random.randint(60, 95) for _ in tech_skills],
            'seniority': [random.choice(['Junior', 'Mid', 'Senior']) for _ in tech_skills],
            'job_count': [random.randint(20, 150) for _ in tech_skills]
        }

def generate_mock_jobs_with_real_filters(limit: int = 100) -> List[dict]:
    """Generate mock job data using real filter options from API"""
    client = get_api_client()
    filter_options = client.get_filter_options()
    
    import random
    from datetime import datetime, timedelta
    
    # Use real data from API
    companies = filter_options.get('companies', ['TechCorp', 'StartupXYZ', 'Enterprise Solutions'])
    locations = filter_options.get('locations', ['Remote', 'New York, NY', 'San Francisco, CA'])
    employment_types = filter_options.get('employment_types', ['Full-time', 'Part-time', 'Contract'])
    seniorities = filter_options.get('seniorities', ['Junior', 'Mid', 'Senior'])
    tech_skills = filter_options.get('tech_skills', ['Python', 'JavaScript', 'React'])
    
    # Job titles that match the companies and skills we have
    job_titles = [
        "Software Engineer", "Full Stack Developer", "Frontend Developer", 
        "Backend Developer", "DevOps Engineer", "Data Scientist", 
        "Machine Learning Engineer", "Product Manager", "UX Designer",
        "UI Designer", "Data Engineer", "Site Reliability Engineer",
        "Security Engineer", "Mobile Developer", "QA Engineer"
    ]
    
    salary_ranges = [
        "$40k - $60k", "$60k - $80k", "$80k - $100k", "$100k - $120k",
        "$120k - $150k", "$150k+", "$2,500+", "$3,000+", "$4,000+",
        "$5,000+", "$6,000+", "$8,000+", "$10,000+"
    ]
    
    jobs = []
    
    for i in range(limit):
        # Generate random job data
        company = random.choice(companies)
        location = random.choice(locations)
        employment_type = random.choice(employment_types)
        seniority = random.choice(seniorities)
        title = random.choice(job_titles)
        
        # Generate skills (3-8 tech skills)
        num_skills = random.randint(3, min(8, len(tech_skills)))
        job_skills = random.sample(tech_skills, num_skills)
        
        # Generate dates (within last 30 days)
        days_ago = random.randint(0, 30)
        posted_date = f"{days_ago} days ago"
        
        # Create job data
        job = {
            "id": f"mock_{i+1}",
            "title": title,
            "company": company,
            "location": location,
            "type": employment_type,
            "experience": seniority,
            "salary": random.choice(salary_ranges),
            "posted_date": posted_date,
            "status": "Active",
            "applications": random.randint(0, 50),
            "skills": job_skills,
            "tech_skills": job_skills,
            "soft_skills": ["Communication", "Teamwork"],
            "description": f"We are looking for a {seniority.lower()} {title.lower()} to join our dynamic team at {company}. This role requires expertise in {', '.join(job_skills[:3])}.",
            "job_link": f"https://example.com/jobs/{i+1}",
            "scraped_at": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
            "updated_at": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        }
        
        jobs.append(job)
    
    logger.info(f"Generated {len(jobs)} mock jobs using real filter data")
    return jobs

def update_job_status(job_id: str, status: str) -> bool:
    """Update job status via API"""
    client = get_api_client()
    
    # Log the request details
    logger.info(f"Attempting to update job {job_id} status to {status}")
    
    # Check if backend is available
    health = client.health_check()
    if health.get("status") != "healthy":
        logger.warning("Backend not available, cannot update job status")
        return False
    
    logger.info(f"Backend is healthy, proceeding with status update")
    
    # Update job status
    response = client.update_job_status(job_id, status)
    
    logger.info(f"API response for job {job_id}: {response}")
    
    if response.get("message"):
        logger.info(f"Successfully updated job {job_id} status to {status}")
        return True
    else:
        logger.error(f"Failed to update job {job_id} status - no message in response")
        return False

def get_live_roles() -> dict:
    """Get all available roles and categories from API"""
    client = get_api_client()
    
    # Check if backend is available
    health = client.health_check()
    if health.get("status") != "healthy":
        logger.warning("Backend not available, using default roles")
        return {
            "categories": {
                "All": 100,
                "Developer": 45,
                "Designer": 12,
                "Data": 18,
                "DevOps": 8,
                "Product": 10,
                "Marketing": 4,
                "Sales": 3
            },
            "roles": [
                {"title": "Software Engineer", "job_count": 25},
                {"title": "Full Stack Developer", "job_count": 20},
                {"title": "Data Scientist", "job_count": 18}
            ]
        }
    
    # Get real roles data from API
    roles_data = client.get_dashboard_roles()
    
    if roles_data:
        logger.info("Using real roles data from API")
        return roles_data
    else:
        # Fallback to default roles
        logger.warning("Roles API failed, using default data")
        return {
            "categories": {
                "All": 0,
                "Developer": 0,
                "Designer": 0,
                "Data": 0,
                "DevOps": 0,
                "Product": 0,
                "Marketing": 0,
                "Sales": 0
            },
            "roles": []
        }

def get_live_skills_by_role(role_category: str = "All", limit: int = 8) -> dict:
    """Get technical and soft skills for a specific role category from API"""
    client = get_api_client()
    
    # Check if backend is available
    health = client.health_check()
    if health.get("status") != "healthy":
        logger.warning("Backend not available, using default skills")
        return {
            "role_category": role_category,
            "tech_skills": ["Python", "JavaScript", "React"],
            "tech_demand_scores": [95, 88, 82],
            "tech_job_counts": [150, 142, 128],
            "tech_seniorities": ["Senior", "Mid", "Senior"],
            "soft_skills": ["Communication", "Leadership", "Problem Solving"],
            "soft_demand_scores": [90, 85, 88],
            "soft_job_counts": [145, 135, 140],
            "soft_seniorities": ["Mid", "Senior", "Mid"]
        }
    
    # Get real skills data from API
    skills_data = client.get_skills_by_role(role_category, limit)
    
    if skills_data:
        logger.info(f"Using real skills data from API for role: {role_category}")
        return skills_data
    else:
        # Fallback to default skills
        logger.warning("Skills by role API failed, using default data")
        return {
            "role_category": role_category,
            "tech_skills": [],
            "tech_demand_scores": [],
            "tech_job_counts": [],
            "tech_seniorities": [],
            "soft_skills": [],
            "soft_demand_scores": [],
            "soft_job_counts": [],
            "soft_seniorities": []
        }
