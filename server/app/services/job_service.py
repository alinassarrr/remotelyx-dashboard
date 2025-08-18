from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorCollection
from app.core.database import get_collection, JOBS_COLLECTION
from app.models.job import ScrapedJob, JobCreate, JobUpdate
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class JobService:
    def __init__(self):
        self.collection: AsyncIOMotorCollection = get_collection(JOBS_COLLECTION)
    
    async def create_job(self, job: JobCreate) -> ScrapedJob:
        """Create a new job posting."""
        try:
            job_dict = job.dict(by_alias=True)
            job_dict["created_at"] = datetime.utcnow()
            job_dict["updated_at"] = datetime.utcnow()
            
            result = await self.collection.insert_one(job_dict)
            job_dict["_id"] = result.inserted_id
            
            return ScrapedJob(**job_dict)
        except Exception as e:
            logger.error(f"Error creating job: {e}")
            raise e
    
    async def get_job_by_id(self, job_id: str) -> Optional[ScrapedJob]:
        """Get a job by its ID."""
        try:
            if not ObjectId.is_valid(job_id):
                return None
            
            job_dict = await self.collection.find_one({"_id": ObjectId(job_id)})
            if job_dict:
                return ScrapedJob(**job_dict)
            return None
        except Exception as e:
            logger.error(f"Error getting job by ID: {e}")
            raise e
    
    async def get_jobs(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        company: Optional[str] = None,
        location: Optional[str] = None,
        seniority: Optional[str] = None,
        employment_type: Optional[str] = None,
        status: Optional[str] = None,
        skills: Optional[List[str]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        sort_by: str = "created_at",
        sort_order: int = -1
    ) -> Tuple[List[ScrapedJob], int]:
        """Get jobs with filtering, search, and pagination."""
        try:
            # Build filter query
            filter_query = {}
            
            if company:
                filter_query["data.company"] = {"$regex": company, "$options": "i"}
            
            if location:
                filter_query["data.location"] = {"$regex": location, "$options": "i"}
            
            if seniority:
                filter_query["data.seniority"] = {"$regex": seniority, "$options": "i"}
            
            if employment_type:
                filter_query["data.employment_type"] = {"$regex": employment_type, "$options": "i"}
            
            if status:
                filter_query["status"] = status
            
            if skills:
                filter_query["$or"] = [
                    {"data.tech_skills": {"$in": skills}},
                    {"data.soft_skills": {"$in": skills}}
                ]
            
            if date_from or date_to:
                date_filter = {}
                if date_from:
                    date_filter["$gte"] = date_from
                if date_to:
                    date_filter["$lte"] = date_to
                filter_query["created_at"] = date_filter
            
            # Text search across multiple fields
            if search:
                filter_query["$text"] = {"$search": search}
            
            # Get total count
            total_count = await self.collection.count_documents(filter_query)
            
            # Build sort query
            sort_query = [(sort_by, sort_order)]
            
            # Execute query with pagination
            cursor = self.collection.find(filter_query).sort(sort_query).skip(skip).limit(limit)
            jobs = []
            
            async for job_dict in cursor:
                jobs.append(ScrapedJob(**job_dict))
            
            return jobs, total_count
            
        except Exception as e:
            logger.error(f"Error getting jobs: {e}")
            raise e
    
    async def update_job(self, job_id: str, job_update: JobUpdate) -> Optional[ScrapedJob]:
        """Update an existing job."""
        try:
            if not ObjectId.is_valid(job_id):
                return None
            
            update_data = job_update.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            result = await self.collection.update_one(
                {"_id": ObjectId(job_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return await self.get_job_by_id(job_id)
            return None
            
        except Exception as e:
            logger.error(f"Error updating job: {e}")
            raise e
    
    async def update_job_status(self, job_id: str, status: str) -> bool:
        """Update job status (NEW, ANALYZED, MATCHED)."""
        try:
            if not ObjectId.is_valid(job_id):
                return False
            
            # Validate status
            if status not in ["NEW", "ANALYZED", "MATCHED"]:
                raise ValueError(f"Invalid status: {status}")
            
            update_data = {
                "status": status,
                "updated_at": datetime.utcnow()
            }
            
            result = await self.collection.update_one(
                {"_id": ObjectId(job_id)},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating job status: {e}")
            raise e
    
    async def delete_job(self, job_id: str) -> bool:
        """Delete a job by ID."""
        try:
            if not ObjectId.is_valid(job_id):
                return False
            
            result = await self.collection.delete_one({"_id": ObjectId(job_id)})
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error deleting job: {e}")
            raise e
    
    async def get_jobs_by_company(self, company: str, limit: int = 50) -> List[ScrapedJob]:
        """Get all jobs from a specific company."""
        try:
            cursor = self.collection.find(
                {"data.company": {"$regex": company, "$options": "i"}}
            ).sort("created_at", -1).limit(limit)
            
            jobs = []
            async for job_dict in cursor:
                jobs.append(ScrapedJob(**job_dict))
            
            return jobs
            
        except Exception as e:
            logger.error(f"Error getting jobs by company: {e}")
            raise e
    
    async def get_recent_jobs(self, days: int = 7, limit: int = 50) -> List[ScrapedJob]:
        """Get recent jobs from the last N days."""
        try:
            date_from = datetime.utcnow() - timedelta(days=days)
            
            cursor = self.collection.find(
                {"created_at": {"$gte": date_from}}
            ).sort("created_at", -1).limit(limit)
            
            jobs = []
            async for job_dict in cursor:
                jobs.append(ScrapedJob(**job_dict))
            
            return jobs
            
        except Exception as e:
            logger.error(f"Error getting recent jobs: {e}")
            raise e
    
    async def get_job_stats(self) -> Dict:
        """Get basic job statistics."""
        try:
            total_jobs = await self.collection.count_documents({})
            
            # Jobs created this week
            week_ago = datetime.utcnow() - timedelta(days=7)
            new_this_week = await self.collection.count_documents({
                "created_at": {"$gte": week_ago}
            })
            
            # Unique companies
            pipeline = [
                {"$group": {"_id": "$data.company"}},
                {"$count": "total"}
            ]
            company_result = await self.collection.aggregate(pipeline).to_list(1)
            unique_companies = company_result[0]["total"] if company_result else 0
            
            # Employment type distribution
            pipeline = [
                {"$group": {"_id": "$data.employment_type", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            employment_types = await self.collection.aggregate(pipeline).to_list(None)
            
            # Seniority distribution
            pipeline = [
                {"$group": {"_id": "$data.seniority", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            seniority_dist = await self.collection.aggregate(pipeline).to_list(None)
            
            return {
                "total_jobs": total_jobs,
                "new_this_week": new_this_week,
                "unique_companies": unique_companies,
                "employment_types": employment_types,
                "seniority_distribution": seniority_dist
            }
            
        except Exception as e:
            logger.error(f"Error getting job stats: {e}")
            raise e
    
    async def bulk_create_jobs(self, jobs: List[JobCreate]) -> List[str]:
        """Create multiple jobs at once."""
        try:
            job_dicts = []
            for job in jobs:
                job_dict = job.dict(by_alias=True)
                job_dict["created_at"] = datetime.utcnow()
                job_dict["updated_at"] = datetime.utcnow()
                job_dicts.append(job_dict)
            
            result = await self.collection.insert_many(job_dicts)
            return [str(id) for id in result.inserted_ids]
            
        except Exception as e:
            logger.error(f"Error bulk creating jobs: {e}")
            raise e 