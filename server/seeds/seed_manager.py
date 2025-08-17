import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.core.database import get_collection
from app.core.security import get_password_hash
from bson import ObjectId

logger = logging.getLogger(__name__)

class SeedManager:
    def __init__(self):
        self.seeds_collection = get_collection("seeds")
        
    async def ensure_seeds_collection(self):
        """Ensure seeds collection exists"""
        await self.seeds_collection.create_index("name", unique=True)
        
    async def get_applied_seeds(self) -> List[str]:
        """Get list of already applied seed names"""
        cursor = self.seeds_collection.find({}, {"name": 1})
        seeds = await cursor.to_list(length=None)
        return [s["name"] for s in seeds]
        
    async def mark_seed_applied(self, name: str, details: Dict[str, Any] = None):
        """Mark a seed as applied"""
        seed_record = {
            "name": name,
            "applied_at": datetime.utcnow(),
            "details": details or {}
        }
        await self.seeds_collection.insert_one(seed_record)
        logger.info(f"Seed '{name}' marked as applied")
        
    async def run_seed(self, name: str, seed_func):
        """Run a specific seed"""
        try:
            logger.info(f"Running seed: {name}")
            await seed_func()
            await self.mark_seed_applied(name)
            logger.info(f"Seed '{name}' completed successfully")
            return True
        except Exception as e:
            logger.error(f"Seed '{name}' failed: {str(e)}")
            raise
            
    async def run_all_seeds(self, force: bool = False):
        """Run all pending seeds"""
        await self.ensure_seeds_collection()
        
        # Get all available seeds
        available_seeds = self.get_available_seeds()
        applied_seeds = await self.get_applied_seeds()
        
        # Find pending seeds
        pending_seeds = [
            name for name in available_seeds 
            if name not in applied_seeds
        ]
        
        if not pending_seeds:
            logger.info("No pending seeds")
            return
            
        logger.info(f"Found {len(pending_seeds)} pending seeds")
        
        # Run seeds in order
        for seed_name in pending_seeds:
            seed_func = self.get_seed_function(seed_name)
            if seed_func:
                await self.run_seed(seed_name, seed_func)
            else:
                logger.warning(f"No seed function found for: {seed_name}")
                
    def get_available_seeds(self) -> List[str]:
        """Get list of all available seed names in order"""
        return [
            "001_create_admin_user",
            "002_create_sample_jobs",
            "003_create_sample_activity_logs"
        ]
        
    def get_seed_function(self, seed_name: str):
        """Get the seed function by name"""
        seed_functions = {
            "001_create_admin_user": self._create_admin_user,
            "002_create_sample_jobs": self._create_sample_jobs,
            "003_create_sample_activity_logs": self._create_sample_activity_logs
        }
        return seed_functions.get(seed_name)
        
    # Seed implementations
    async def _create_admin_user(self):
        """Create default admin user"""
        users_collection = get_collection("users")
        
        # Check if admin already exists
        existing_admin = await users_collection.find_one({"email": "admin@remotelyx.com"})
        if existing_admin:
            logger.info("Admin user already exists, skipping")
            return
            
        admin_user = {
            "email": "admin@remotelyx.com",
            "password_hash": get_password_hash("admin123"),
            "role": "admin",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        await users_collection.insert_one(admin_user)
        logger.info("Admin user created: admin@remotelyx.com / admin123")
        
    async def _create_sample_jobs(self):
        """Create sample job postings for testing"""
        jobs_collection = get_collection("jobs")
        
        # Check if jobs already exist
        existing_jobs = await jobs_collection.count_documents({})
        if existing_jobs > 0:
            logger.info("Sample jobs already exist, skipping")
            return
            
        sample_jobs = [
            {
                "title": "Senior Backend Engineer",
                "company": "TechCorp",
                "location": "Remote",
                "type": "remote",
                "seniority": "senior",
                "salary_min": 120000,
                "salary_max": 180000,
                "skills": ["Python", "FastAPI", "MongoDB", "Docker", "AWS"],
                "posting_date": datetime.utcnow() - timedelta(days=5),
                "status": "new",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "title": "Full Stack Developer",
                "company": "StartupXYZ",
                "location": "San Francisco",
                "type": "hybrid",
                "seniority": "mid",
                "salary_min": 90000,
                "salary_max": 130000,
                "skills": ["JavaScript", "React", "Node.js", "PostgreSQL"],
                "posting_date": datetime.utcnow() - timedelta(days=3),
                "status": "new",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "title": "Data Scientist",
                "company": "DataTech Inc",
                "location": "New York",
                "type": "onsite",
                "seniority": "senior",
                "salary_min": 110000,
                "salary_max": 160000,
                "skills": ["Python", "Machine Learning", "SQL", "Statistics", "TensorFlow"],
                "posting_date": datetime.utcnow() - timedelta(days=1),
                "status": "new",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "title": "DevOps Engineer",
                "company": "CloudSolutions",
                "location": "Remote",
                "type": "remote",
                "seniority": "mid",
                "salary_min": 95000,
                "salary_max": 140000,
                "skills": ["Docker", "Kubernetes", "AWS", "Terraform", "Linux"],
                "posting_date": datetime.utcnow() - timedelta(days=2),
                "status": "new",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "title": "Frontend Developer",
                "company": "WebDesign Pro",
                "location": "Austin",
                "type": "hybrid",
                "seniority": "junior",
                "salary_min": 65000,
                "salary_max": 85000,
                "skills": ["HTML", "CSS", "JavaScript", "React", "TypeScript"],
                "posting_date": datetime.utcnow() - timedelta(days=4),
                "status": "new",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        await jobs_collection.insert_many(sample_jobs)
        logger.info(f"Created {len(sample_jobs)} sample jobs")
        
    async def _create_sample_activity_logs(self):
        """Create sample activity logs for testing"""
        activity_collection = get_collection("activity_logs")
        
        # Check if logs already exist
        existing_logs = await activity_collection.count_documents({})
        if existing_logs > 0:
            logger.info("Sample activity logs already exist, skipping")
            return
            
        # Get some job IDs for reference
        jobs_collection = get_collection("jobs")
        jobs = await jobs_collection.find({}, {"_id": 1}).limit(3).to_list(length=None)
        job_ids = [job["_id"] for job in jobs] if jobs else []
        
        sample_logs = [
            {
                "event": "system_startup",
                "timestamp": datetime.utcnow() - timedelta(hours=2),
                "details": {"version": "1.0.0", "environment": "development"}
            },
            {
                "event": "sample_data_created",
                "timestamp": datetime.utcnow() - timedelta(hours=1),
                "details": {"type": "jobs", "count": 5}
            }
        ]
        
        # Add job-specific logs if jobs exist
        for i, job_id in enumerate(job_ids):
            sample_logs.append({
                "event": "job_created",
                "timestamp": datetime.utcnow() - timedelta(minutes=30 + i * 10),
                "job_id": job_id,
                "details": {"source": "seed_data"}
            })
            
        await activity_collection.insert_many(sample_logs)
        logger.info(f"Created {len(sample_logs)} sample activity logs") 