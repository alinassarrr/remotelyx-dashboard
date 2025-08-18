#!/usr/bin/env python3
"""
Database Setup Script for RemotelyX Backend
This script will clear the database and set up fresh collections with sample data.
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta
import random

sys.path.append(os.path.dirname(__file__))

from app.core.database import connect_to_mongo, close_mongo_connection, get_collection
from app.services.seeder_service import SeederService
from app.services.analytics_service import AnalyticsService
from app.models.job import JobCreate, JobData

async def setup_database():
    """Set up the database with fresh collections and data."""
    try:
        print("🚀 Setting up RemotelyX Database...")
        
        # Connect to MongoDB
        await connect_to_mongo()
        print("✅ Connected to MongoDB")
        
        # Get collections
        db = get_collection("jobs").database
        jobs_collection = get_collection("jobs")
        analytics_collection = get_collection("analytics")
        
        # Clear all collections
        print("🗑️  Clearing existing collections...")
        await jobs_collection.delete_many({})
        await analytics_collection.delete_many({})
        print("✅ Collections cleared")
        
        # Create fresh indexes
        print("🔧 Recreating database indexes...")
        await create_indexes(jobs_collection)
        print("✅ Indexes recreated")
        
        # Generate comprehensive job data
        print("📊 Generating comprehensive job data...")
        jobs = generate_comprehensive_jobs()
        
        # Create jobs in batches
        batch_size = 25
        total_jobs = len(jobs)
        
        for i in range(0, total_jobs, batch_size):
            batch = jobs[i:i + batch_size]
            job_creates = []
            
            for job_data in batch:
                job_create = JobCreate(
                    data=job_data,
                    message="Job created for frontend dashboard",
                    scraped_at=datetime.utcnow().isoformat(),
                    success=True
                )
                job_creates.append(job_create)
            
            # Bulk create jobs
            job_ids = await bulk_create_jobs(job_creates)
            print(f"   ✅ Created batch {i//batch_size + 1}: {len(job_ids)} jobs")
        
        print(f"\n🎉 Successfully created {total_jobs} jobs!")
        
        # Generate analytics data
        print("\n📈 Generating analytics data...")
        analytics_service = AnalyticsService()
        analytics_data = await analytics_service.generate_full_analytics()
        print(f"✅ Analytics generated and cached")
        
        # Verify the setup
        print("\n🔍 Verifying database setup...")
        total_jobs_count = await jobs_collection.count_documents({})
        analytics_count = await analytics_collection.count_documents({})
        
        print(f"\n📊 Database Setup Complete:")
        print(f"   Total Jobs: {total_jobs_count}")
        print(f"   Analytics Records: {analytics_count}")
        print(f"   Database: {db.name}")
        print(f"   Collections: {await db.list_collection_names()}")
        
        await close_mongo_connection()
        print("\n✅ Database connection closed")
        print("\n🎯 Database setup completed successfully!")
        print("\n📖 Next steps:")
        print("   1. Start your backend server: ./start.sh")
        print("   2. Test the APIs at: http://localhost:8000/docs")
        print("   3. Your frontend now has all the data it needs!")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

async def create_indexes(collection):
    """Create database indexes for optimal performance."""
    try:
        # Text search index
        await collection.create_index([
            ("data.title", "text"),
            ("data.company", "text"),
            ("data.description", "text"),
            ("data.tech_skills", "text"),
            ("data.soft_skills", "text")
        ])
        
        # Single field indexes
        await collection.create_index("data.company", 1)
        await collection.create_index("data.location", 1)
        await collection.create_index("data.seniority", 1)
        await collection.create_index("data.employment_type", 1)
        await collection.create_index("created_at", -1)
        
        # Compound indexes
        await collection.create_index([
            ("created_at", -1),
            ("data.company", 1)
        ])
        
    except Exception as e:
        print(f"⚠️  Warning: Some indexes may already exist: {e}")

async def bulk_create_jobs(jobs):
    """Create multiple jobs at once."""
    try:
        collection = get_collection("jobs")
        job_dicts = []
        
        for job in jobs:
            job_dict = job.dict(by_alias=True)
            job_dict["created_at"] = datetime.utcnow()
            job_dict["updated_at"] = datetime.utcnow()
            job_dicts.append(job_dict)
        
        result = await collection.insert_many(job_dicts)
        return [str(id) for id in result.inserted_ids]
        
    except Exception as e:
        print(f"❌ Error in bulk create: {e}")
        return []

def generate_comprehensive_jobs():
    """Generate comprehensive job data for the frontend."""
    
    # Companies that match frontend expectations
    companies = [
        "TechCorp", "StartupXYZ", "Enterprise Solutions", "Innovation Labs", 
        "Digital Dynamics", "CloudBase", "DataWorks", "CyberSec Pro", 
        "DevOps Hub", "Productify", "Creative Studios", "Analytics Pro",
        "Mobile First", "AI Ventures", "Blockchain Tech", "Green Energy Co",
        "HealthTech", "FinTech Solutions", "EduTech", "Retail Innovations",
        "Gamma", "Microsoft", "Google", "Amazon", "Apple", "Meta", "Netflix"
    ]
    
    # Locations from frontend
    locations = [
        "Remote", "New York, NY", "San Francisco, CA", "Austin, TX", 
        "Seattle, WA", "Boston, MA", "Denver, CO", "Chicago, IL",
        "Los Angeles, CA", "Miami, FL", "Portland, OR", "Atlanta, GA"
    ]
    
    # Employment types from frontend
    employment_types = [
        "Full-time", "Part-time", "Contract", "Freelance", "Internship"
    ]
    
    # Seniority levels from frontend
    seniority_levels = [
        "Junior", "Mid", "Senior", "Lead", "Principal", "Executive"
    ]
    
    # Tech skills that match frontend top skills
    tech_skills = [
        "Python", "JavaScript", "React", "Node.js", "Java", "C++", "C#", "Go",
        "TypeScript", "Vue.js", "Angular", "Django", "Flask", "Spring Boot",
        "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Terraform",
        "MongoDB", "PostgreSQL", "MySQL", "Redis", "Elasticsearch",
        "Machine Learning", "Data Analysis", "Statistics", "R", "TensorFlow",
        "PyTorch", "Git", "CI/CD", "Jenkins", "GitHub Actions", "Linux",
        "Shell Scripting", "REST APIs", "GraphQL", "Microservices"
    ]
    
    # Soft skills from frontend
    soft_skills = [
        "Communication", "Leadership", "Teamwork", "Problem Solving",
        "Critical Thinking", "Adaptability", "Time Management", "Creativity",
        "Analytical Skills", "Customer Focus", "Collaboration", "Innovation"
    ]
    
    # Job titles from frontend
    job_titles = [
        "Software Engineer", "Full Stack Developer", "Frontend Developer", 
        "Backend Developer", "DevOps Engineer", "Data Scientist", 
        "Machine Learning Engineer", "Product Manager", "UX Designer",
        "UI Designer", "Data Engineer", "Site Reliability Engineer",
        "Security Engineer", "Mobile Developer", "QA Engineer"
    ]
    
    # Salary ranges from frontend
    salary_ranges = [
        "$40k - $60k", "$60k - $80k", "$80k - $100k", "$100k - $120k",
        "$120k - $150k", "$150k+", "$2,500+", "$3,000+", "$4,000+",
        "$5,000+", "$6,000+", "$8,000+", "$10,000+"
    ]
    
    jobs = []
    
    # Generate jobs with realistic distribution
    for i in range(150):  # Create 150 jobs for good frontend testing
        
        # Randomize job data
        company = random.choice(companies)
        location = random.choice(locations)
        employment_type = random.choice(employment_types)
        seniority = random.choice(seniority_levels)
        title = random.choice(job_titles)
        
        # Generate skills (3-8 tech skills, 2-5 soft skills)
        num_tech_skills = random.randint(3, 8)
        num_soft_skills = random.randint(2, 5)
        
        job_tech_skills = random.sample(tech_skills, num_tech_skills)
        job_soft_skills = random.sample(soft_skills, num_soft_skills)
        
        # Generate random dates (within last 30 days)
        days_ago = random.randint(0, 30)
        created_date = datetime.utcnow() - timedelta(days=days_ago)
        
        # Create realistic description
        description = f"We are looking for a {seniority.lower()} {title.lower()} to join our dynamic team at {company}. "
        description += f"This role requires expertise in {', '.join(job_tech_skills[:3])}. "
        description += "This is an exciting opportunity to work on cutting-edge projects and grow your career."
        
        # Create job data
        job_data = JobData(
            company=company,
            date_posted=f"{days_ago} days ago",
            description=description,
            employment_type=employment_type,
            job_link=f"https://example.com/jobs/{i+1}",
            location=location,
            salary=random.choice(salary_ranges),
            scraped_at=created_date.strftime("%a, %d %b %Y %H:%M:%S GMT"),
            seniority=seniority,
            soft_skills=job_soft_skills,
            tech_skills=job_tech_skills,
            title=title,
            updated_at=created_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
        )
        
        jobs.append(job_data)
    
    # Add the example n8n job from requirements
    example_job = JobData(
        company="Gamma",
        date_posted="Not specified",
        description="We are looking for a highly skilled Full-Stack Developer with 3+ years of experience to join our dynamic team and help build an AI SaaS platform in the ALCOHOLIC BEVERAGE niche. Develop and maintain full-stack web applications using React.js/Next.js (Frontend), Node.js/ Nest.js (Backend). Design and manage databases using MySQL and Vector Databases for optimized performance. Develop and integrate APIs to connect various services and applications. Work with AI tools to enhance application features, including AI-driven automation, chatbots, and data processing. Deploy and manage applications on AWS, ensuring scalability, security, and high availability. Optimize front-end performance, ensuring smooth UI/UX experiences. Implement authentication and security best practices, including OAuth, JWT, and data encryption. Work with DevOps tools for CI/CD, containerization (Docker), and server management. Troubleshoot and debug application issues, ensuring high performance and reliability.",
        employment_type="Full-time",
        job_link="https://gamma.app/docs/full-stack-developer-ic-3s64m1oqf3nuf5u?mode=doc.",
        location="Remote",
        salary="$2,500+",
        scraped_at=datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
        seniority="Mid",
        soft_skills=["communication", "leadership", "teamwork", "problem-solving"],
        tech_skills=["React.js", "Next.js", "Node.js", "Nest.js", "MySQL", "PostgreSQL", "Vector DB", "AWS", "Docker", "CI/CD Pipelines", "OpenAI APIs", "LangChain", "GraphQL"],
        title="Full Stack Developer - IC",
        updated_at=datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    )
    jobs.append(example_job)
    
    print(f"   📝 Generated {len(jobs)} comprehensive job postings")
    print(f"   🏢 Companies: {len(set(job.company for job in jobs))}")
    print(f"   🌍 Locations: {len(set(job.location for job in jobs))}")
    print(f"   💼 Seniority levels: {len(set(job.seniority for job in jobs))}")
    print(f"   🛠️  Tech skills: {len(set(skill for job in jobs for skill in job.tech_skills))}")
    
    return jobs

if __name__ == "__main__":
    asyncio.run(setup_database()) 