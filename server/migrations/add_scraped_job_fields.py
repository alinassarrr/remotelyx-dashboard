"""
Migration: Add scraped job fields
Date: 2024-08-17
Description: Add new fields to support scraped job data including description, employment_type, 
job_link, salary as string, tech_skills, soft_skills, and scraped_at timestamp.
"""

from datetime import datetime
import asyncio
from app.core.database import get_database

async def migrate_up():
    """Add new fields to jobs collection"""
    db = await get_database()
    jobs_collection = db["jobs"]
    
    print("Starting migration: Add scraped job fields")
    
    # Update all existing jobs to include new fields with default values
    update_result = await jobs_collection.update_many(
        {},  # Update all documents
        {
            "$set": {
                # Add new optional fields with None defaults
                "description": None,
                "employment_type": None,
                "job_link": None,
                "salary": None,
                "date_posted": None,
                "tech_skills": [],
                "soft_skills": [],
                "scraped_at": None,
                
                # Make existing required fields optional for backward compatibility
                "posting_date": None  # Will be set to None for jobs without this field
            },
            "$unset": {
                # Remove any fields that might cause issues (if they exist)
            }
        }
    )
    
    print(f"Updated {update_result.modified_count} existing jobs with new fields")
    
    # Update skills field to combine with tech_skills and soft_skills where they exist
    async for job in jobs_collection.find({}):
        combined_skills = []
        
        # Combine existing skills
        if job.get("skills"):
            combined_skills.extend(job["skills"])
        
        # Add tech_skills if they exist
        if job.get("tech_skills"):
            combined_skills.extend(job["tech_skills"])
        
        # Add soft_skills if they exist
        if job.get("soft_skills"):
            combined_skills.extend(job["soft_skills"])
        
        # Remove duplicates and update
        unique_skills = list(set(combined_skills))
        
        if unique_skills != job.get("skills", []):
            await jobs_collection.update_one(
                {"_id": job["_id"]},
                {"$set": {"skills": unique_skills}}
            )
    
    # Create indexes for new fields
    try:
        await jobs_collection.create_index("job_link")
        await jobs_collection.create_index("scraped_at")
        await jobs_collection.create_index("tech_skills")
        await jobs_collection.create_index("employment_type")
        print("Created indexes for new fields")
    except Exception as e:
        print(f"Warning: Could not create some indexes: {e}")
    
    # Update migration history
    migrations_collection = db["migrations"]
    await migrations_collection.insert_one({
        "name": "add_scraped_job_fields",
        "applied_at": datetime.utcnow(),
        "description": "Add new fields to support scraped job data"
    })
    
    print("Migration completed successfully")


async def migrate_down():
    """Remove scraped job fields (rollback)"""
    db = await get_database()
    jobs_collection = db["jobs"]
    
    print("Rolling back migration: Remove scraped job fields")
    
    # Remove the new fields
    update_result = await jobs_collection.update_many(
        {},
        {
            "$unset": {
                "description": "",
                "employment_type": "",
                "job_link": "",
                "salary": "",
                "date_posted": "",
                "tech_skills": "",
                "soft_skills": "",
                "scraped_at": ""
            }
        }
    )
    
    print(f"Removed new fields from {update_result.modified_count} jobs")
    
    # Drop indexes
    try:
        await jobs_collection.drop_index("job_link_1")
        await jobs_collection.drop_index("scraped_at_1")
        await jobs_collection.drop_index("tech_skills_1")
        await jobs_collection.drop_index("employment_type_1")
        print("Dropped indexes for scraped job fields")
    except Exception as e:
        print(f"Warning: Could not drop some indexes: {e}")
    
    # Remove from migration history
    migrations_collection = db["migrations"]
    await migrations_collection.delete_one({"name": "add_scraped_job_fields"})
    
    print("Migration rollback completed")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "down":
        asyncio.run(migrate_down())
    else:
        asyncio.run(migrate_up()) 