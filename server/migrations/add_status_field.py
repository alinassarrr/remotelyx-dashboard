#!/usr/bin/env python3
"""
Migration script to add status field to all existing jobs in the database.
This will add a 'status' field with default value 'NEW' to all job documents.
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the parent directory to the Python path so we can import our app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import db, connect_to_mongo
from app.core.config import settings

async def add_status_field():
    """Add status field to all existing jobs."""
    try:
        await connect_to_mongo()
        
        jobs_collection = db.db.jobs
        
        # Count total jobs
        total_jobs = await jobs_collection.count_documents({})
        print(f"Found {total_jobs} jobs in database")
        
        # Count jobs without status field
        jobs_without_status = await jobs_collection.count_documents({
            'status': {'$exists': False}
        })
        print(f"Jobs without status field: {jobs_without_status}")
        
        if jobs_without_status == 0:
            print("All jobs already have status field. Migration not needed.")
            return
        
        # Add status field to all jobs that don't have it
        print("Adding status field to jobs...")
        result = await jobs_collection.update_many(
            {'status': {'$exists': False}},  # Filter: jobs without status
            {
                '$set': {
                    'status': 'NEW',  # Default status
                    'updated_at': datetime.utcnow()  # Update the timestamp
                }
            }
        )
        
        print(f"✅ Successfully updated {result.modified_count} jobs with status field")
        
        # Verify the migration
        jobs_with_status = await jobs_collection.count_documents({
            'status': {'$exists': True}
        })
        print(f"Jobs now with status field: {jobs_with_status}")
        
        # Show sample of updated jobs
        print("\nSample of updated jobs:")
        sample_jobs = await jobs_collection.find({
            'status': {'$exists': True}
        }).limit(3).to_list(length=3)
        
        for i, job in enumerate(sample_jobs, 1):
            print(f"Job {i}: status = {job.get('status')}, company = {job.get('data', {}).get('company', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        raise e

if __name__ == "__main__":
    print("🔄 Starting status field migration...")
    asyncio.run(add_status_field())
    print("✅ Migration completed!")
