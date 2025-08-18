from fastapi import APIRouter, HTTPException, Query, Path, Depends
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.services.job_service import JobService
from app.models.job import ScrapedJob, JobCreate, JobUpdate
from app.models.analytics import DashboardStats
import logging

logger = logging.getLogger(__name__)

# Request/Response models
class JobStatusUpdate(BaseModel):
    status: str

router = APIRouter(prefix="/jobs", tags=["jobs"])

# Dependency to get job service
def get_job_service():
    return JobService()

@router.post("/", response_model=ScrapedJob, status_code=201)
async def create_job(
    job: JobCreate,
    job_service: JobService = Depends(get_job_service)
):
    """Create a new job posting."""
    try:
        created_job = await job_service.create_job(job)
        return created_job
    except Exception as e:
        logger.error(f"Error creating job: {e}")
        raise HTTPException(status_code=500, detail="Failed to create job")

@router.post("/bulk", response_model=List[str], status_code=201)
async def bulk_create_jobs(
    jobs: List[JobCreate],
    job_service: JobService = Depends(get_job_service)
):
    """Create multiple jobs at once."""
    try:
        job_ids = await job_service.bulk_create_jobs(jobs)
        return job_ids
    except Exception as e:
        logger.error(f"Error bulk creating jobs: {e}")
        raise HTTPException(status_code=500, detail="Failed to create jobs")

@router.get("/", response_model=dict)
async def get_jobs(
    skip: int = Query(0, ge=0, description="Number of jobs to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of jobs to return"),
    search: Optional[str] = Query(None, description="Search term for job title, company, description, or skills"),
    company: Optional[str] = Query(None, description="Filter by company name"),
    location: Optional[str] = Query(None, description="Filter by location"),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    employment_type: Optional[str] = Query(None, description="Filter by employment type"),
    status: Optional[str] = Query(None, description="Filter by job status (NEW, ANALYZED, MATCHED)"),
    skills: Optional[str] = Query(None, description="Comma-separated list of skills to filter by"),
    date_from: Optional[str] = Query(None, description="Filter jobs created from this date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter jobs created until this date (YYYY-MM-DD)"),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: int = Query(-1, ge=-1, le=1, description="Sort order: -1 for descending, 1 for ascending"),
    job_service: JobService = Depends(get_job_service)
):
    """Get jobs with filtering, search, and pagination."""
    try:
        # Parse skills list
        skills_list = None
        if skills:
            skills_list = [s.strip() for s in skills.split(",") if s.strip()]
        
        # Parse dates
        date_from_dt = None
        date_to_dt = None
        if date_from:
            try:
                date_from_dt = datetime.strptime(date_from, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date_from format. Use YYYY-MM-DD")
        
        if date_to:
            try:
                date_to_dt = datetime.strptime(date_to, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date_to format. Use YYYY-MM-DD")
        
        # Validate sort_by field
        allowed_sort_fields = [
            "created_at", "updated_at", "data.company", "data.location", 
            "data.seniority", "data.employment_type"
        ]
        if sort_by not in allowed_sort_fields:
            sort_by = "created_at"
        
        jobs, total_count = await job_service.get_jobs(
            skip=skip,
            limit=limit,
            search=search,
            company=company,
            location=location,
            seniority=seniority,
            employment_type=employment_type,
            status=status,
            skills=skills_list,
            date_from=date_from_dt,
            date_to=date_to_dt,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        return {
            "jobs": jobs,
            "total_count": total_count,
            "skip": skip,
            "limit": limit,
            "has_more": (skip + limit) < total_count
        }
        
    except Exception as e:
        logger.error(f"Error getting jobs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve jobs")

@router.get("/{job_id}", response_model=ScrapedJob)
async def get_job(
    job_id: str,
    job_service: JobService = Depends(get_job_service)
):
    """Get a specific job by ID."""
    try:
        job = await job_service.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve job")

@router.put("/{job_id}", response_model=ScrapedJob)
async def update_job(
    job_id: str,
    job_update: JobUpdate,
    job_service: JobService = Depends(get_job_service)
):
    """Update an existing job."""
    try:
        updated_job = await job_service.update_job(job_id, job_update)
        if not updated_job:
            raise HTTPException(status_code=404, detail="Job not found")
        return updated_job
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating job {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update job")


@router.delete("/{job_id}", status_code=204)
async def delete_job(
    job_id: str,
    job_service: JobService = Depends(get_job_service)
):
    """Delete a job by ID."""
    try:
        success = await job_service.delete_job(job_id)
        if not success:
            raise HTTPException(status_code=404, detail="Job not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting job {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete job")

@router.patch("/{job_id}/status", response_model=dict)
async def update_job_status(
    job_id: str,
    status_update: JobStatusUpdate,
    job_service: JobService = Depends(get_job_service)
):
    """Update job status (NEW, ANALYZED, MATCHED)."""
    try:
        if status_update.status not in ["NEW", "ANALYZED", "MATCHED"]:
            raise HTTPException(status_code=400, detail="Invalid status. Must be NEW, ANALYZED, or MATCHED")
        
        success = await job_service.update_job_status(job_id, status_update.status)
        if not success:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return {"message": f"Job status updated to {status_update.status}", "job_id": job_id, "status": status_update.status}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating job status {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update job status")

@router.get("/company/{company_name}", response_model=List[ScrapedJob])
async def get_jobs_by_company(
    company_name: str,
    limit: int = Query(50, ge=1, le=1000, description="Maximum number of jobs to return"),
    job_service: JobService = Depends(get_job_service)
):
    """Get all jobs from a specific company."""
    try:
        jobs = await job_service.get_jobs_by_company(company_name, limit)
        return jobs
    except Exception as e:
        logger.error(f"Error getting jobs for company {company_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve company jobs")

@router.get("/recent/{days}", response_model=List[ScrapedJob])
async def get_recent_jobs(
    days: int = Path(ge=1, le=365, description="Number of days to look back"),
    limit: int = Query(50, ge=1, le=1000, description="Maximum number of jobs to return"),
    job_service: JobService = Depends(get_job_service)
):
    """Get recent jobs from the last N days."""
    try:
        jobs = await job_service.get_recent_jobs(days, limit)
        return jobs
    except Exception as e:
        logger.error(f"Error getting recent jobs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve recent jobs")

@router.get("/stats/overview", response_model=dict)
async def get_job_stats(
    job_service: JobService = Depends(get_job_service)
):
    """Get basic job statistics."""
    try:
        stats = await job_service.get_job_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting job stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve job statistics")

@router.get("/filters/options", response_model=dict)
async def get_filter_options(
    job_service: JobService = Depends(get_job_service)
):
    """Get available filter options for the frontend."""
    try:
        # Get distinct values for filters
        pipeline = [
            {"$group": {"_id": "$data.company"}},
            {"$sort": {"_id": 1}}
        ]
        companies = await job_service.collection.aggregate(pipeline).to_list(None)
        
        pipeline = [
            {"$group": {"_id": "$data.location"}},
            {"$sort": {"_id": 1}}
        ]
        locations = await job_service.collection.aggregate(pipeline).to_list(None)
        
        pipeline = [
            {"$group": {"_id": "$data.seniority"}},
            {"$sort": {"_id": 1}}
        ]
        seniorities = await job_service.collection.aggregate(pipeline).to_list(None)
        
        pipeline = [
            {"$group": {"_id": "$data.employment_type"}},
            {"$sort": {"_id": 1}}
        ]
        employment_types = await job_service.collection.aggregate(pipeline).to_list(None)
        
        pipeline = [
            {"$unwind": "$data.tech_skills"},
            {"$group": {"_id": "$data.tech_skills"}},
            {"$sort": {"_id": 1}}
        ]
        tech_skills = await job_service.collection.aggregate(pipeline).to_list(None)
        
        pipeline = [
            {"$unwind": "$data.soft_skills"},
            {"$group": {"_id": "$data.soft_skills"}},
            {"$sort": {"_id": 1}}
        ]
        soft_skills = await job_service.collection.aggregate(pipeline).to_list(None)
        
        # Status options (predefined)
        status_options = ["NEW", "ANALYZED", "MATCHED"]
        
        return {
            "companies": [item["_id"] for item in companies if item["_id"]],
            "locations": [item["_id"] for item in locations if item["_id"]],
            "seniorities": [item["_id"] for item in seniorities if item["_id"]],
            "employment_types": [item["_id"] for item in employment_types if item["_id"]],
            "tech_skills": [item["_id"] for item in tech_skills if item["_id"]],
            "soft_skills": [item["_id"] for item in soft_skills if item["_id"]],
            "status_options": status_options
        }
        
    except Exception as e:
        logger.error(f"Error getting filter options: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve filter options") 