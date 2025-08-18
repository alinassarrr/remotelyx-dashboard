#!/usr/bin/env python3
"""
Simple Frontend Data Seeder for RemotelyX Dashboard
"""
import asyncio
import sys
import os
from datetime import datetime
import random

sys.path.append(os.path.dirname(__file__))

from app.core.database import connect_to_mongo, close_mongo_connection
from app.services.seeder_service import SeederService
from app.services.analytics_service import AnalyticsService
from app.models.job import JobCreate, JobData

async def seed_data():
    """Seed database with frontend data."""
    try:
        print("🚀 Starting data seeding...")
        
        await connect_to_mongo()
        print("✅ Connected to MongoDB")
        
        seeder = SeederService()
        
        # Clear existing data
        print("🗑️  Clearing existing data...")
        await seeder.clear_all_jobs()
        
        # Generate sample jobs
        print("📊 Creating sample jobs...")
        jobs = generate_sample_jobs()
        
        # Create jobs
        for i, job_data in enumerate(jobs):
            job_create = JobCreate(
                data=job_data,
                message=f"Job {i+1} created",
                scraped_at=datetime.utcnow().isoformat(),
                success=True
            )
            await seeder.create_job(job_create)
            if (i + 1) % 10 == 0:
                print(f"   ✅ Created {i+1} jobs...")
        
        print(f"🎉 Created {len(jobs)} jobs!")
        
        # Generate analytics
        print("📈 Generating analytics...")
        analytics_service = AnalyticsService()
        await analytics_service.generate_full_analytics()
        
        await close_mongo_connection()
        print("✅ Seeding completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def generate_sample_jobs():
    """Generate sample job data."""
    companies = ["TechCorp", "StartupXYZ", "Gamma", "Microsoft", "Google"]
    locations = ["Remote", "New York, NY", "San Francisco, CA"]
    skills = ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker"]
    
    jobs = []
    for i in range(100):
        job_data = JobData(
            company=random.choice(companies),
            date_posted=f"{random.randint(0, 30)} days ago",
            description=f"Sample job description {i+1}",
            employment_type="Full-time",
            job_link=f"https://example.com/job/{i+1}",
            location=random.choice(locations),
            salary="$80k - $120k",
            scraped_at=datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
            seniority=random.choice(["Junior", "Mid", "Senior"]),
            soft_skills=["Communication", "Teamwork"],
            tech_skills=random.sample(skills, random.randint(3, 5)),
            title=f"Developer {i+1}",
            updated_at=datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        )
        jobs.append(job_data)
    
    return jobs

if __name__ == "__main__":
    asyncio.run(seed_data()) 