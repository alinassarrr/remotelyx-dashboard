#!/usr/bin/env python3
"""
Script to add sample scraped job data to MongoDB for testing
"""

import asyncio
import requests
import json
from datetime import datetime

# Sample scraped job data matching your scraper format
sample_scraped_jobs = {
    "jobs": [
        {
            "data": {
                "company": "Gamma",
                "date_posted": "Not specified",
                "description": "We are looking for a highly skilled Full-Stack Developer with 3+ years of experience to join our dynamic team and help build an AI SaaS platform in the ALCOHOLIC BEVERAGE niche. Develop and maintain full-stack web applications using React.js/Next.js (Frontend), Node.js/Nest.js (Backend). Design and manage databases using MySQL and Vector Databases for optimized performance. Develop and integrate APIs to connect various services and applications. Work with AI tools to enhance application features.",
                "employment_type": "Full-time",
                "job_link": "https://gamma.app/docs/full-stack-developer-ic-3s64m1oqf3nuf5u?mode=doc",
                "location": "Remote",
                "salary": "$2,500+",
                "scraped_at": "Sun, 17 Aug 2025 00:02:43 GMT",
                "seniority": "Mid",
                "soft_skills": ["communication", "leadership", "teamwork", "problem-solving"],
                "tech_skills": ["React.js", "Next.js", "Node.js", "Nest.js", "MySQL", "PostgreSQL", "Vector DB", "AWS", "Docker", "CI/CD Pipelines", "OpenAI APIs", "LangChain", "GraphQL"],
                "title": "Full Stack Developer - IC",
                "updated_at": "Sun, 17 Aug 2025 00:02:43 GMT"
            },
            "message": "Job updated successfully (ID: 68a11b52c7310ba19285064a)",
            "scraped_at": "2025-08-17T00:02:43.608904",
            "success": True
        },
        {
            "data": {
                "company": "TechStartup Inc",
                "date_posted": "2024-08-15",
                "description": "Join our growing startup as a backend engineer. Work with cutting-edge technology to build scalable microservices. You'll be responsible for designing APIs, implementing business logic, and ensuring system performance. Experience with cloud platforms and containerization is required.",
                "employment_type": "Full-time",
                "job_link": "https://techstartup.com/careers/backend-engineer-001",
                "location": "San Francisco, CA (Remote OK)",
                "salary": "$4,000-7,000",
                "scraped_at": "Sun, 17 Aug 2025 01:15:30 GMT",
                "seniority": "Mid",
                "soft_skills": ["communication", "initiative", "analytical thinking"],
                "tech_skills": ["Python", "Django", "PostgreSQL", "Redis", "Kubernetes", "Docker", "AWS", "Git"],
                "title": "Backend Engineer",
                "updated_at": "Sun, 17 Aug 2025 01:15:30 GMT"
            },
            "message": "Job scraped successfully",
            "scraped_at": "2025-08-17T01:15:30.123456",
            "success": True
        },
        {
            "data": {
                "company": "CloudTech Solutions",
                "date_posted": "2024-08-16",
                "description": "We're seeking a Senior Frontend Developer to lead our UI/UX initiatives. You'll work closely with designers and backend teams to create responsive, accessible web applications. Knowledge of modern JavaScript frameworks and state management is essential.",
                "employment_type": "Full-time",
                "job_link": "https://cloudtech.com/jobs/senior-frontend-dev",
                "location": "Remote",
                "salary": "$3,500-5,500",
                "scraped_at": "Sun, 17 Aug 2025 02:30:15 GMT",
                "seniority": "Senior",
                "soft_skills": ["creativity", "attention to detail", "collaboration"],
                "tech_skills": ["React", "TypeScript", "CSS3", "HTML5", "Redux", "Webpack", "Jest", "Figma"],
                "title": "Senior Frontend Developer",
                "updated_at": "Sun, 17 Aug 2025 02:30:15 GMT"
            },
            "message": "Job scraped successfully",
            "scraped_at": "2025-08-17T02:30:15.789012",
            "success": True
        },
        {
            "data": {
                "company": "DataFlow Analytics",
                "date_posted": "2024-08-14",
                "description": "Looking for a Data Engineer to build and maintain our data pipeline infrastructure. You'll work with large datasets, implement ETL processes, and ensure data quality. Experience with big data technologies and cloud platforms is preferred.",
                "employment_type": "Full-time",
                "job_link": "https://dataflow.com/careers/data-engineer",
                "location": "Austin, TX (Hybrid)",
                "salary": "$5,000-8,000",
                "scraped_at": "Sun, 17 Aug 2025 03:45:20 GMT",
                "seniority": "Senior",
                "soft_skills": ["problem-solving", "analytical thinking", "communication"],
                "tech_skills": ["Python", "Apache Spark", "Kafka", "Airflow", "AWS", "Snowflake", "SQL", "Pandas"],
                "title": "Senior Data Engineer",
                "updated_at": "Sun, 17 Aug 2025 03:45:20 GMT"
            },
            "message": "Job scraped successfully",
            "scraped_at": "2025-08-17T03:45:20.345678",
            "success": True
        },
        {
            "data": {
                "company": "MobileFirst Studio",
                "date_posted": "2024-08-13",
                "description": "We're hiring a React Native Developer to build cross-platform mobile applications. You'll be responsible for developing new features, optimizing performance, and ensuring a smooth user experience across iOS and Android platforms.",
                "employment_type": "Full-time",
                "job_link": "https://mobilefirst.studio/jobs/react-native-dev",
                "location": "Remote",
                "salary": "$3,000-4,500",
                "scraped_at": "Sun, 17 Aug 2025 04:20:10 GMT",
                "seniority": "Mid",
                "soft_skills": ["attention to detail", "teamwork", "adaptability"],
                "tech_skills": ["React Native", "JavaScript", "iOS", "Android", "Redux", "Firebase", "Git", "Jest"],
                "title": "React Native Developer",
                "updated_at": "Sun, 17 Aug 2025 04:20:10 GMT"
            },
            "message": "Job scraped successfully",
            "scraped_at": "2025-08-17T04:20:10.901234",
            "success": True
        }
    ]
}

def add_sample_data():
    """Add sample scraped job data via API"""
    try:
        print("🚀 Adding sample scraped job data...")
        
        # Make sure the server is running
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        if health_response.status_code != 200:
            print("❌ Backend server is not running. Please start it first:")
            print("   cd server && ./run_dev.sh")
            return False
        
        print("✅ Backend server is running")
        
        # Import the sample data
        response = requests.post(
            "http://localhost:8000/api/v1/scraped-jobs/import",
            json=sample_scraped_jobs,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Sample data imported successfully!")
            print(f"   Total jobs: {result['total_jobs']}")
            print(f"   Successful: {result['successful_imports']}")
            print(f"   Failed: {result['failed_imports']}")
            print(f"   Created: {len(result['created_jobs'])}")
            print(f"   Updated: {len(result['updated_jobs'])}")
            
            if result['errors']:
                print(f"   Errors: {result['errors']}")
            
            return True
        else:
            print(f"❌ Import failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        print("   Make sure the backend server is running on http://localhost:8000")
        return False

def check_database_content():
    """Check what's in the database"""
    try:
        print("\n📊 Checking database content...")
        
        # Get jobs
        response = requests.get("http://localhost:8000/api/v1/jobs", timeout=10)
        if response.status_code == 200:
            jobs = response.json()
            print(f"✅ Found {len(jobs)} jobs in database")
            
            for i, job in enumerate(jobs[:3], 1):  # Show first 3 jobs
                print(f"\n   Job {i}:")
                print(f"     Title: {job.get('title')}")
                print(f"     Company: {job.get('company')}")
                print(f"     Location: {job.get('location')}")
                print(f"     Salary: {job.get('salary', 'N/A')}")
                print(f"     Tech Skills: {job.get('tech_skills', [])[:3]}...")
                print(f"     Scraped: {'Yes' if job.get('scraped_at') else 'No'}")
            
            if len(jobs) > 3:
                print(f"   ... and {len(jobs) - 3} more jobs")
                
        # Get scraping stats
        response = requests.get("http://localhost:8000/api/v1/scraped-jobs/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print(f"\n📈 Scraping Statistics:")
            print(f"   Total jobs: {stats['total_jobs']}")
            print(f"   Scraped jobs: {stats['scraped_jobs']}")
            print(f"   Manual jobs: {stats['manual_jobs']}")
            print(f"   Coverage: {stats['scraping_coverage']}%")
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")

if __name__ == "__main__":
    print("🧪 RemotelyX Dashboard - Sample Data Importer")
    print("=" * 50)
    
    if add_sample_data():
        check_database_content()
        print("\n🎉 Sample data setup complete!")
        print("\n💡 Next steps:")
        print("   1. Check the API at: http://localhost:8000/docs")
        print("   2. View jobs: http://localhost:8000/api/v1/jobs")
        print("   3. Check stats: http://localhost:8000/api/v1/scraped-jobs/stats")
        print("   4. Test your frontend with the new data!")
    else:
        print("\n❌ Failed to add sample data")
        print("   Please check that the backend server is running and try again") 