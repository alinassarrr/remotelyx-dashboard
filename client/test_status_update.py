#!/usr/bin/env python3

import sys
import logging
from api_client import update_job_status, get_live_jobs

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_status_update():
    """Test the status update functionality"""
    print("Testing job status update functionality...")
    
    # First, get a job to test with
    print("\n1. Getting a job to test with...")
    jobs = get_live_jobs(limit=1)
    
    if not jobs:
        print("ERROR: No jobs found!")
        return False
    
    job = jobs[0]
    job_id = job['id']
    current_status = job.get('status', 'NEW')
    
    print(f"Found job: {job_id}")
    print(f"Title: {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Current status: {current_status}")
    
    # Determine new status to test with
    status_options = ["NEW", "ANALYZED", "MATCHED"]
    new_status = None
    for status in status_options:
        if status != current_status:
            new_status = status
            break
    
    if not new_status:
        new_status = "ANALYZED"  # fallback
    
    print(f"\n2. Attempting to update status from {current_status} to {new_status}...")
    
    # Test the update
    success = update_job_status(job_id, new_status)
    
    print(f"\n3. Update result: {'SUCCESS' if success else 'FAILED'}")
    
    if success:
        # Verify the update worked by fetching the job again
        print("\n4. Verifying update by fetching job again...")
        updated_jobs = get_live_jobs(limit=1000)  # Get more jobs to find our specific one
        updated_job = None
        
        for j in updated_jobs:
            if j['id'] == job_id:
                updated_job = j
                break
        
        if updated_job:
            updated_status = updated_job.get('status', 'UNKNOWN')
            print(f"Job status after update: {updated_status}")
            
            if updated_status == new_status:
                print("✅ SUCCESS: Status was updated correctly!")
                return True
            else:
                print(f"❌ FAILED: Expected {new_status}, but got {updated_status}")
                return False
        else:
            print("❌ FAILED: Could not find the job after update")
            return False
    else:
        print("❌ FAILED: Status update returned False")
        return False

if __name__ == "__main__":
    test_status_update()
