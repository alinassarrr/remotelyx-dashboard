#!/usr/bin/env python3
"""
Frontend Data Seeder for RemotelyX Dashboard
This script populates the database with all the data structures needed by the frontend.
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta
import random

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

from app.core.database import connect_to_mongo, close_mongo_connection
from app.services.seeder_service import SeederService
from app.services.analytics_service import AnalyticsService
from app.models.job import JobCreate, JobData

async def seed_frontend_data():
    """Seed the database with comprehensive frontend data."""
    try:
        print("🚀 Starting Frontend Data Seeding...")
        
        # Connect to MongoDB
        await connect_to_mongo()
        print("✅ Connected to MongoDB")
        
        # Get services
        seeder = SeederService()
        analytics_service = AnalyticsService()
        
        # Clear existing data
        print("\n🗑️  Clearing existing data...")
        await seeder.clear_all_jobs()
        print("✅ Database cleared")
        
        # Seed comprehensive job data
        print("\n📊 Seeding comprehensive job data...")
        
        # Generate realistic job data based on frontend requirements
        jobs = generate_frontend_jobs()
        
        # Create jobs in batches
        batch_size = 50
        total_jobs = len(jobs)
        
        for i in range(0, total_jobs, batch_size):
            batch = jobs[i:i + batch_size]
            job_creates = []
            
            for job_data in batch:
                job_create = JobCreate(
                    data=job_data,
                    message="Job created for frontend testing",
                    scraped_at=datetime.utcnow().isoformat(),
                    success=True
                )
                job_creates.append(job_create)
            
            # Bulk create jobs
            job_ids = await seeder.bulk_create_jobs(job_creates)
            print(f"   ✅ Created batch {i//batch_size + 1}: {len(job_ids)} jobs")
        
        print(f"\n🎉 Successfully created {total_jobs} jobs!")
        
        # Generate analytics data
        print("\n📈 Generating analytics data...")
        analytics_data = await analytics_service.generate_full_analytics()
        print(f"✅ Analytics generated and cached")
        
        # Verify the data
        print("\n🔍 Verifying seeded data...")
        status = await seeder.get_seeding_status()
        
        print(f"\n📊 Final Database Status:")
        print(f"   Total Jobs: {status['total_jobs']}")
        print(f"   Has Data: {status['has_data']}")
        print(f"   Sample Jobs: {status['sample_jobs_count']}")
        print(f"   Last Updated: {status['last_updated']}")
        
        await close_mongo_connection()
        print("\n✅ Database connection closed")
        print("\n🎯 Frontend data seeding completed successfully!")
        print("\n📖 Next steps:")
        print("   1. Start your backend server: ./start.sh")
        print("   2. Test the APIs at: http://localhost:8000/docs")
        print("   3. Your frontend should now have all the data it needs!")
        
    except Exception as e:
        print(f"❌ Error seeding frontend data: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def generate_frontend_jobs():
    """Generate comprehensive job data that matches frontend requirements."""
    
    # Companies that match frontend expectations
    companies = [
        "TechCorp", "StartupXYZ", "Enterprise Solutions", "Innovation Labs", 
        "Digital Dynamics", "CloudBase", "DataWorks", "CyberSec Pro", 
        "DevOps Hub", "Productify", "Creative Studios", "Analytics Pro",
        "Mobile First", "AI Ventures", "Blockchain Tech", "Green Energy Co",
        "HealthTech", "FinTech Solutions", "EduTech", "Retail Innovations",
        "Gamma", "Microsoft", "Google", "Amazon", "Apple", "Meta", "Netflix",
        "Uber", "Airbnb", "Stripe", "Shopify", "Slack", "Zoom", "Discord"
    ]
    
    # Locations that match frontend filters
    locations = [
        "Remote", "New York, NY", "San Francisco, CA", "Austin, TX", 
        "Seattle, WA", "Boston, MA", "Denver, CO", "Chicago, IL",
        "Los Angeles, CA", "Miami, FL", "Portland, OR", "Atlanta, GA",
        "Toronto, Canada", "London, UK", "Berlin, Germany", "Amsterdam, Netherlands",
        "Sydney, Australia", "Tokyo, Japan", "Singapore", "Dubai, UAE"
    ]
    
    # Employment types from frontend
    employment_types = [
        "Full-time", "Part-time", "Contract", "Freelance", "Internship"
    ]
    
    # Seniority levels that match frontend expectations
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
        "Shell Scripting", "REST APIs", "GraphQL", "Microservices",
        "React.js", "Next.js", "Nest.js", "Vector DB", "OpenAI APIs", "LangChain"
    ]
    
    # Soft skills from frontend
    soft_skills = [
        "Communication", "Leadership", "Teamwork", "Problem Solving",
        "Critical Thinking", "Adaptability", "Time Management", "Creativity",
        "Analytical Skills", "Customer Focus", "Collaboration", "Innovation",
        "Strategic Thinking", "Decision Making", "Conflict Resolution"
    ]
    
    # Job titles that match frontend expectations
    job_titles = [
        "Software Engineer", "Full Stack Developer", "Frontend Developer", 
        "Backend Developer", "DevOps Engineer", "Data Scientist", 
        "Machine Learning Engineer", "Product Manager", "UX Designer",
        "UI Designer", "Data Engineer", "Site Reliability Engineer",
        "Security Engineer", "Mobile Developer", "QA Engineer",
        "Technical Lead", "Engineering Manager", "Solutions Architect",
        "Full Stack Developer - IC", "AI Engineer", "Cloud Architect"
    ]
    
    # Salary ranges that match frontend filters
    salary_ranges = [
        "$40k - $60k", "$60k - $80k", "$80k - $100k", "$100k - $120k",
        "$120k - $150k", "$150k+", "$2,500+", "$3,000+", "$4,000+",
        "$5,000+", "$6,000+", "$8,000+", "$10,000+"
    ]
    
    # Generate jobs with realistic distribution
    jobs = []
    
    # Create jobs with specific patterns to match frontend expectations
    
    # 1. High-demand skills jobs (Python, JavaScript, React)
    high_demand_skills = ["Python", "JavaScript", "React", "AWS", "Docker"]
    for skill in high_demand_skills:
        for _ in range(random.randint(15, 25)):  # 15-25 jobs per high-demand skill
            company = random.choice(companies)
            location = random.choice(locations)
            seniority = random.choice(["Mid", "Senior", "Lead"])
            employment_type = random.choice(["Full-time", "Contract"])
            
            # Create job with this skill as primary
            job_skills = [skill] + random.sample([s for s in tech_skills if s != skill], random.randint(2, 6))
            soft_skills_list = random.sample(soft_skills, random.randint(2, 4))
            
            # Generate realistic description
            description = f"We are looking for a {seniority.lower()} developer with strong {skill} skills to join our team at {company}. "
            description += f"Experience with {', '.join(job_skills[1:3])} is required. "
            description += "This is an exciting opportunity to work on cutting-edge projects and grow your career."
            
            # Create job data
            job_data = JobData(
                company=company,
                date_posted=f"{random.randint(0, 30)} days ago",
                description=description,
                employment_type=employment_type,
                job_link=f"https://example.com/jobs/{len(jobs)+1}",
                location=location,
                salary=random.choice(salary_ranges),
                scraped_at=datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                seniority=seniority,
                soft_skills=soft_skills_list,
                tech_skills=job_skills,
                title=random.choice(job_titles),
                updated_at=datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
            )
            
            jobs.append(job_data)
    
    # 2. Junior level jobs
    for _ in range(30):
        company = random.choice(companies)
        location = random.choice(locations)
        seniority = "Junior"
        employment_type = random.choice(["Full-time", "Internship"])
        
        job_skills = random.sample(tech_skills, random.randint(3, 5))
        soft_skills_list = random.sample(soft_skills, random.randint(2, 3))
        
        description = f"Entry-level position for a {seniority.lower()} developer at {company}. "
        description += f"Basic knowledge of {', '.join(job_skills[:2])} required. "
        description += "Great opportunity for recent graduates to start their career."
        
        job_data = JobData(
            company=company,
            date_posted=f"{random.randint(0, 30)} days ago",
            description=description,
            employment_type=employment_type,
            job_link=f"https://example.com/jobs/{len(jobs)+1}",
            location=location,
            salary=random.choice(["$40k - $60k", "$60k - $80k", "$2,500+", "$3,000+"]),
            scraped_at=datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
            seniority=seniority,
            soft_skills=soft_skills_list,
            tech_skills=job_skills,
            title=random.choice(job_titles),
            updated_at=datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        )
        
        jobs.append(job_data)
    
    # 3. Executive/Lead positions
    for _ in range(20):
        company = random.choice(companies[:10])  # Top companies for executive roles
        location = random.choice(locations[:5])  # Major cities
        seniority = random.choice(["Lead", "Principal", "Executive"])
        employment_type = "Full-time"
        
        job_skills = random.sample(tech_skills, random.randint(4, 7))
        soft_skills_list = random.sample(soft_skills, random.randint(3, 5))
        
        description = f"Senior {seniority.lower()} position at {company}. "
        description += f"Requires expertise in {', '.join(job_skills[:3])} and strong leadership skills. "
        description += "This role involves strategic decision-making and team leadership."
        
        job_data = JobData(
            company=company,
            date_posted=f"{random.randint(0, 30)} days ago",
            description=description,
            employment_type=employment_type,
            job_link=f"https://example.com/jobs/{len(jobs)+1}",
            location=location,
            salary=random.choice(["$120k - $150k", "$150k+", "$8,000+", "$10,000+"]),
            scraped_at=datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
            seniority=seniority,
            soft_skills=soft_skills_list,
            tech_skills=job_skills,
            title=random.choice(["Technical Lead", "Engineering Manager", "Solutions Architect", "CTO"]),
            updated_at=datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        )
        
        jobs.append(job_data)
    
    # 4. Specialized roles (Data, DevOps, Design)
    specialized_roles = [
        ("Data Scientist", ["Python", "Machine Learning", "Statistics", "SQL"]),
        ("DevOps Engineer", ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux"]),
        ("UX Designer", ["Figma", "User Research", "Prototyping", "Design Systems"]),
        ("Product Manager", ["Product Strategy", "User Research", "Analytics", "Agile"])
    ]
    
    for role, skills in specialized_roles:
        for _ in range(random.randint(8, 15)):
            company = random.choice(companies)
            location = random.choice(locations)
            seniority = random.choice(["Mid", "Senior"])
            employment_type = random.choice(["Full-time", "Contract"])
            
            job_skills = skills + random.sample([s for s in tech_skills if s not in skills], random.randint(1, 3))
            soft_skills_list = random.sample(soft_skills, random.randint(2, 4))
            
            description = f"We are seeking a {seniority.lower()} {role.lower()} to join {company}. "
            description += f"Strong expertise in {', '.join(skills[:2])} required. "
            description += "This role involves working closely with cross-functional teams."
            
            job_data = JobData(
                company=company,
                date_posted=f"{random.randint(0, 30)} days ago",
                description=description,
                employment_type=employment_type,
                job_link=f"https://example.com/jobs/{len(jobs)+1}",
                location=location,
                salary=random.choice(salary_ranges[2:6]),  # Mid to high range
                scraped_at=datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                seniority=seniority,
                soft_skills=soft_skills_list,
                tech_skills=job_skills,
                title=role,
                updated_at=datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
            )
            
            jobs.append(job_data)
    
    # 5. Add the example n8n job from requirements
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
    
    # Shuffle jobs to make them appear in random order
    random.shuffle(jobs)
    
    print(f"   📝 Generated {len(jobs)} realistic job postings")
    print(f"   🏢 Companies: {len(set(job.company for job in jobs))}")
    print(f"   🌍 Locations: {len(set(job.location for job in jobs))}")
    print(f"   💼 Seniority levels: {len(set(job.seniority for job in jobs))}")
    print(f"   🛠️  Tech skills: {len(set(skill for job in jobs for skill in job.tech_skills))}")
    
    return jobs

if __name__ == "__main__":
    asyncio.run(seed_frontend_data()) 