"""
Database management for MongoDB operations
"""
import json
import logging
from datetime import datetime
from typing import Dict, Any, Tuple
from pymongo import MongoClient
from bson import ObjectId
from config import MONGODB_URI, DATABASE_NAME, COLLECTION_NAME

logger = logging.getLogger(__name__)


class CustomJSONEncoder(json.JSONEncoder):
    """JSON encoder for MongoDB ObjectId"""
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


class DatabaseManager:
    """Handles MongoDB connection and operations"""
    
    def __init__(self):
        try:
            self.client = MongoClient(MONGODB_URI)
            self.db = self.client[DATABASE_NAME]
            self.collection = self.db[COLLECTION_NAME]
            logger.info("✅ Connected to MongoDB successfully")
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            self.client = None
    
    def save_job(self, job_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Save job data to MongoDB"""
        try:
            if not self.client:
                return False, "Database not connected"
            
            # Add timestamp
            job_data['scraped_at'] = datetime.now()
            job_data['updated_at'] = datetime.now()
            
            # Check if job already exists (by job_link)
            existing_job = self.collection.find_one({'job_link': job_data['job_link']})
            
            if existing_job:
                # Update existing job
                job_data['updated_at'] = datetime.now()
                result = self.collection.update_one(
                    {'job_link': job_data['job_link']},
                    {'$set': job_data}
                )
                logger.info(f"📝 Updated existing job: {job_data['title']}")
                return True, f"Job updated successfully (ID: {existing_job['_id']})"
            else:
                # Insert new job
                result = self.collection.insert_one(job_data)
                logger.info(f"💾 Saved new job: {job_data['title']}")
                return True, f"Job saved successfully (ID: {result.inserted_id})"
                
        except Exception as e:
            logger.error(f"❌ Error saving job: {e}")
            return False, str(e)
    
    def get_jobs(self, limit: int = 10, skip: int = 0) -> Dict[str, Any]:
        """Get jobs from database"""
        try:
            if not self.client:
                return {"error": "Database not connected"}
            
            jobs = list(self.collection.find(
                {},
                {'_id': 0}  # Exclude MongoDB _id field
            ).sort('scraped_at', -1).skip(skip).limit(limit))
            
            return {
                "success": True,
                "jobs": jobs,
                "count": len(jobs),
                "limit": limit,
                "skip": skip
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_job_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            if not self.client:
                return {"error": "Database not connected"}
            
            total_jobs = self.collection.count_documents({})
            recent_jobs = self.collection.count_documents({
                'scraped_at': {'$gte': datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)}
            })
            
            return {
                "total_jobs": total_jobs,
                "jobs_today": recent_jobs,
                "database": DATABASE_NAME,
                "collection": COLLECTION_NAME
            }
        except Exception as e:
            return {"error": str(e)}
