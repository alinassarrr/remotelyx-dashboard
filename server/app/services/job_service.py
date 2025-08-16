from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.core.database import get_collection
from app.models.job_model import JobModel
from app.schemas.job_schema import JobCreate, JobUpdate, JobResponse, JobFilter
from bson import ObjectId

class JobService:
    def __init__(self):
        self.collection = get_collection("jobs")

    async def create_job(self, job_data: JobCreate) -> JobResponse:
        """Create a new job"""
        job_dict = job_data.dict()
        job_dict["posting_date"] = datetime.utcnow()
        job_dict["created_at"] = datetime.utcnow()
        job_dict["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(job_dict)
        job_dict["_id"] = result.inserted_id
        
        return JobResponse(
            id=str(result.inserted_id),
            title=job_dict["title"],
            company=job_dict["company"],
            location=job_dict["location"],
            type=job_dict["type"],
            seniority=job_dict["seniority"],
            salary_min=job_dict["salary_min"],
            salary_max=job_dict["salary_max"],
            skills=job_dict["skills"],
            posting_date=job_dict["posting_date"],
            status=job_dict["status"],
            days_to_fill=job_dict["days_to_fill"],
            matched_date=job_dict["matched_date"],
            created_at=job_dict["created_at"],
            updated_at=job_dict["updated_at"]
        )

    async def get_jobs(self, filters: JobFilter, skip: int = 0, limit: int = 100) -> List[JobResponse]:
        """Get jobs with filters"""
        query = {}
        
        if filters.status:
            query["status"] = filters.status
        if filters.skills:
            query["skills"] = {"$in": filters.skills}
        if filters.seniority:
            query["seniority"] = filters.seniority
        if filters.company:
            query["company"] = {"$regex": filters.company, "$options": "i"}
        if filters.location:
            query["location"] = {"$regex": filters.location, "$options": "i"}
        if filters.type:
            query["type"] = filters.type
        if filters.salary_min is not None:
            query["salary_max"] = {"$gte": filters.salary_min}
        if filters.salary_max is not None:
            query["salary_min"] = {"$lte": filters.salary_max}
        if filters.date_from:
            query["posting_date"] = {"$gte": filters.date_from}
        if filters.date_to:
            if "posting_date" in query:
                query["posting_date"]["$lte"] = filters.date_to
            else:
                query["posting_date"] = {"$lte": filters.date_to}
        
        cursor = self.collection.find(query).skip(skip).limit(limit).sort("posting_date", -1)
        jobs = []
        
        async for job in cursor:
            jobs.append(JobResponse(
                id=str(job["_id"]),
                title=job["title"],
                company=job["company"],
                location=job["location"],
                type=job["type"],
                seniority=job["seniority"],
                salary_min=job["salary_min"],
                salary_max=job["salary_max"],
                skills=job["skills"],
                posting_date=job["posting_date"],
                status=job["status"],
                days_to_fill=job.get("days_to_fill"),
                matched_date=job.get("matched_date"),
                created_at=job["created_at"],
                updated_at=job["updated_at"]
            ))
        
        return jobs

    async def get_job_by_id(self, job_id: str) -> Optional[JobResponse]:
        """Get job by ID"""
        try:
            job = await self.collection.find_one({"_id": ObjectId(job_id)})
            if not job:
                return None
            
            return JobResponse(
                id=str(job["_id"]),
                title=job["title"],
                company=job["company"],
                location=job["location"],
                type=job["type"],
                seniority=job["seniority"],
                salary_min=job["salary_min"],
                salary_max=job["salary_max"],
                skills=job["skills"],
                posting_date=job["posting_date"],
                status=job["status"],
                days_to_fill=job.get("days_to_fill"),
                matched_date=job.get("matched_date"),
                created_at=job["created_at"],
                updated_at=job["updated_at"]
            )
        except:
            return None

    async def update_job(self, job_id: str, job_data: JobUpdate) -> Optional[JobResponse]:
        """Update job"""
        try:
            update_data = job_data.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            result = await self.collection.update_one(
                {"_id": ObjectId(job_id)},
                {"$set": update_data}
            )
            
            if result.modified_count == 0:
                return None
            
            return await self.get_job_by_id(job_id)
        except:
            return None

    async def delete_job(self, job_id: str) -> bool:
        """Delete job"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(job_id)})
            return result.deleted_count > 0
        except:
            return False

    async def get_jobs_count(self, filters: JobFilter = None) -> int:
        """Get total count of jobs with filters"""
        query = {}
        if filters:
            # Apply same filters as get_jobs
            if filters.status:
                query["status"] = filters.status
            if filters.skills:
                query["skills"] = {"$in": filters.skills}
            if filters.seniority:
                query["seniority"] = filters.seniority
            if filters.company:
                query["company"] = {"$regex": filters.company, "$options": "i"}
            if filters.location:
                query["location"] = {"$regex": filters.location, "$options": "i"}
            if filters.type:
                query["type"] = filters.type
            if filters.salary_min is not None:
                query["salary_max"] = {"$gte": filters.salary_min}
            if filters.salary_max is not None:
                query["salary_min"] = {"$lte": filters.salary_max}
            if filters.date_from:
                query["posting_date"] = {"$gte": filters.date_from}
            if filters.date_to:
                if "posting_date" in query:
                    query["posting_date"]["$lte"] = filters.date_to
                else:
                    query["posting_date"] = {"$lte": filters.date_to}
        
        return await self.collection.count_documents(query) 