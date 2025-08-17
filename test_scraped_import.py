#!/usr/bin/env python3
"""
Test script for RemotelyX Dashboard scraped job import functionality
Tests both bulk and single job import endpoints
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
HEALTH_ENDPOINT = f"{BASE_URL}/health"
BULK_IMPORT_ENDPOINT = f"{BASE_URL}/api/v1/scraped-jobs/import"
SINGLE_IMPORT_ENDPOINT = f"{BASE_URL}/api/v1/scraped-jobs/import/single"
STATS_ENDPOINT = f"{BASE_URL}/api/v1/scraped-jobs/stats"

def check_server_health():
    """Check if the backend server is running"""
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and healthy")
            return True
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Please make sure the backend server is running on http://localhost:8000")
        return False

def test_single_job_import():
    """Test importing a single job"""
    print("\n🧪 Testing single job import...")
    
    # Sample scraped job data matching your scraper format
    single_job = {
        "data": {
            "company": "TestCorp",
            "date_posted": "2024-08-17",
            "description": "We are looking for a talented developer to join our remote team. You will work on exciting projects using modern technologies.",
            "employment_type": "Full-time",
            "job_link": "https://testcorp.com/careers/senior-dev-001",
            "location": "Remote",
            "salary": "$3,000-5,000",
            "scraped_at": "Sun, 17 Aug 2025 12:00:00 GMT",
            "seniority": "Senior",
            "soft_skills": ["communication", "teamwork", "problem-solving"],
            "tech_skills": ["Python", "FastAPI", "React", "MongoDB", "Docker"],
            "title": "Senior Full-Stack Developer",
            "updated_at": "Sun, 17 Aug 2025 12:00:00 GMT"
        },
        "message": "Job scraped successfully",
        "scraped_at": "2025-08-17T12:00:00.000000",
        "success": True
    }
    
    try:
        response = requests.post(
            SINGLE_IMPORT_ENDPOINT,
            json=single_job,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Single job import successful!")
            print(f"   Action: {result['action']}")
            print(f"   Job ID: {result['job_id']}")
            print(f"   Message: {result['message']}")
            return result['job_id']
        else:
            print(f"❌ Single job import failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Single job import error: {e}")
        return None

def test_bulk_job_import():
    """Test importing multiple jobs in bulk"""
    print("\n🧪 Testing bulk job import...")
    
    # Sample bulk data matching your scraper format
    bulk_jobs = {
        "jobs": [
            {
                "data": {
                    "company": "Gamma",
                    "date_posted": "Not specified",
                    "description": "We are looking for a highly skilled Full-Stack Developer with 3+ years of experience to join our dynamic team and help build an AI SaaS platform in the ALCOHOLIC BEVERAGE niche.",
                    "employment_type": "Full-time",
                    "job_link": "https://gamma.app/docs/full-stack-developer-ic-3s64m1oqf3nuf5u?mode=doc",
                    "location": "Remote",
                    "salary": "$2,500+",
                    "scraped_at": "Sun, 17 Aug 2025 00:02:43 GMT",
                    "seniority": "Mid",
                    "soft_skills": ["communication", "leadership", "teamwork", "problem-solving"],
                    "tech_skills": ["React.js", "Next.js", "Node.js", "Nest.js", "MySQL", "PostgreSQL", "Vector DB", "AWS", "Docker"],
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
                    "description": "Join our growing startup as a backend engineer. Work with cutting-edge technology.",
                    "employment_type": "Full-time",
                    "job_link": "https://techstartup.com/careers/backend-engineer",
                    "location": "San Francisco, CA (Remote OK)",
                    "salary": "$4,000-7,000",
                    "scraped_at": "Sun, 17 Aug 2025 01:15:30 GMT",
                    "seniority": "Mid",
                    "soft_skills": ["communication", "initiative"],
                    "tech_skills": ["Python", "Django", "PostgreSQL", "Redis", "Kubernetes"],
                    "title": "Backend Engineer",
                    "updated_at": "Sun, 17 Aug 2025 01:15:30 GMT"
                },
                "message": "Job scraped successfully",
                "scraped_at": "2025-08-17T01:15:30.123456",
                "success": True
            }
        ]
    }
    
    try:
        response = requests.post(
            BULK_IMPORT_ENDPOINT,
            json=bulk_jobs,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Bulk job import successful!")
            print(f"   Total jobs: {result['total_jobs']}")
            print(f"   Successful: {result['successful_imports']}")
            print(f"   Failed: {result['failed_imports']}")
            print(f"   Created jobs: {len(result['created_jobs'])}")
            print(f"   Updated jobs: {len(result['updated_jobs'])}")
            print(f"   Message: {result['message']}")
            
            if result['errors']:
                print(f"   Errors: {result['errors']}")
                
            return result
        else:
            print(f"❌ Bulk job import failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Bulk job import error: {e}")
        return None

def test_import_stats():
    """Test getting import statistics"""
    print("\n🧪 Testing import statistics...")
    
    try:
        response = requests.get(STATS_ENDPOINT, timeout=5)
        
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Import statistics retrieved!")
            print(f"   Total jobs: {stats['total_jobs']}")
            print(f"   Scraped jobs: {stats['scraped_jobs']}")
            print(f"   Manual jobs: {stats['manual_jobs']}")
            print(f"   Recently scraped: {stats['recently_scraped']}")
            print(f"   Scraping coverage: {stats['scraping_coverage']}%")
            return stats
        else:
            print(f"❌ Stats retrieval failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Stats retrieval error: {e}")
        return None

def test_duplicate_detection():
    """Test duplicate detection by importing the same job twice"""
    print("\n🧪 Testing duplicate detection...")
    
    # First import
    job_data = {
        "data": {
            "company": "DuplicateTest Corp",
            "date_posted": "2024-08-17",
            "description": "This is a test job for duplicate detection.",
            "employment_type": "Full-time",
            "job_link": "https://duplicatetest.com/job-123",
            "location": "Remote",
            "salary": "$5,000",
            "scraped_at": "Sun, 17 Aug 2025 14:00:00 GMT",
            "seniority": "Mid",
            "soft_skills": ["communication"],
            "tech_skills": ["Python", "FastAPI"],
            "title": "Duplicate Test Job",
            "updated_at": "Sun, 17 Aug 2025 14:00:00 GMT"
        },
        "message": "First import",
        "scraped_at": "2025-08-17T14:00:00.000000",
        "success": True
    }
    
    # Import first time
    print("   Importing job for the first time...")
    first_response = requests.post(SINGLE_IMPORT_ENDPOINT, json=job_data)
    
    if first_response.status_code == 200:
        first_result = first_response.json()
        print(f"   First import: {first_result['action']} (ID: {first_result['job_id']})")
        
        # Import second time (should update)
        print("   Importing the same job again...")
        job_data["message"] = "Second import - should update"
        job_data["data"]["salary"] = "$5,500"  # Change salary to test update
        
        second_response = requests.post(SINGLE_IMPORT_ENDPOINT, json=job_data)
        
        if second_response.status_code == 200:
            second_result = second_response.json()
            print(f"   Second import: {second_result['action']} (ID: {second_result['job_id']})")
            
            if first_result['job_id'] == second_result['job_id'] and second_result['action'] == 'updated':
                print("✅ Duplicate detection working correctly!")
                return True
            else:
                print("❌ Duplicate detection not working properly")
                return False
        else:
            print(f"❌ Second import failed: {second_response.status_code}")
            return False
    else:
        print(f"❌ First import failed: {first_response.status_code}")
        return False

def main():
    """Run all tests"""
    print("🚀 RemotelyX Dashboard - Scraped Job Import Tests")
    print("=" * 55)
    
    # Check server health first
    if not check_server_health():
        return
    
    # Run tests
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Single job import
    if test_single_job_import():
        tests_passed += 1
    
    # Test 2: Bulk job import  
    if test_bulk_job_import():
        tests_passed += 1
    
    # Test 3: Import statistics
    if test_import_stats():
        tests_passed += 1
    
    # Test 4: Duplicate detection
    if test_duplicate_detection():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your scraped job import functionality is working correctly!")
    else:
        print(f"⚠️  {total_tests - tests_passed} test(s) failed. Check the output above for details.")
        
    print("\n💡 Next steps:")
    print("   1. Use the API endpoints to import your scraped job data")
    print("   2. Check import statistics regularly")
    print("   3. Monitor server logs for any issues")
    print("   4. Test with your actual scraper data format")

if __name__ == "__main__":
    main() 