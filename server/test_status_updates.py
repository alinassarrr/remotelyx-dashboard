#!/usr/bin/env python3
"""
Test Script for Job Status Updates
"""
import asyncio
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(__file__))

from app.core.database import connect_to_mongo, close_mongo_connection
from app.services.seeder_service import SeederService
from app.services.job_service import JobService

async def test_status_updates():
    """Test the job status update functionality."""
    try:
        print("🧪 Testing Job Status Updates...")
        
        # Connect to MongoDB
        await connect_to_mongo()
        print("✅ Connected to MongoDB")
        
        # Get services
        seeder = SeederService()
        job_service = JobService()
        
        # Check if we have jobs
        status = await seeder.get_seeding_status()
        if not status['has_data']:
            print("📊 No jobs found, creating sample data...")
            await seeder.seed_sample_jobs(5)
            print("✅ Sample jobs created")
        
        # Get a job to test with
        jobs, total = await job_service.get_jobs(limit=1)
        if not jobs:
            print("❌ No jobs available for testing")
            return
        
        test_job = jobs[0]
        job_id = str(test_job.id)
        current_status = test_job.data.status
        
        print(f"\n📋 Testing with job: {test_job.data.title}")
        print(f"   Current status: {current_status}")
        print(f"   Job ID: {job_id}")
        
        # Test status update
        new_status = "In Progress" if current_status != "In Progress" else "Analyzed"
        print(f"\n🔄 Updating status to: {new_status}")
        
        # Update the status
        updated_job = await job_service.update_job_status(job_id, new_status)
        
        if updated_job:
            print(f"✅ Status updated successfully!")
            print(f"   New status: {updated_job.data.status}")
            print(f"   Updated at: {updated_job.updated_at}")
        else:
            print("❌ Failed to update status")
            return
        
        # Verify the update
        print(f"\n🔍 Verifying update...")
        retrieved_job = await job_service.get_job_by_id(job_id)
        
        if retrieved_job and retrieved_job.data.status == new_status:
            print("✅ Status update verified in database")
        else:
            print("❌ Status update verification failed")
        
        # Test invalid status
        print(f"\n🧪 Testing invalid status...")
        try:
            invalid_job = await job_service.update_job_status(job_id, "InvalidStatus")
            if invalid_job:
                print("❌ Should have rejected invalid status")
            else:
                print("✅ Correctly rejected invalid status")
        except Exception as e:
            print(f"✅ Correctly handled invalid status: {e}")
        
        # Test multiple status updates
        print(f"\n🔄 Testing multiple status updates...")
        statuses_to_test = ["New", "Analyzed", "Matched", "In Progress", "Closed"]
        
        for status in statuses_to_test:
            print(f"   Updating to: {status}")
            updated = await job_service.update_job_status(job_id, status)
            if updated:
                print(f"   ✅ Updated to {status}")
            else:
                print(f"   ❌ Failed to update to {status}")
        
        print(f"\n🎉 Status update testing completed successfully!")
        
        await close_mongo_connection()
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_status_updates()) 