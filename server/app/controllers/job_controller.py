from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional
from app.services.job_service import JobService
from app.schemas.job_schema import JobCreate, JobUpdate, JobResponse, JobFilter
from app.controllers.auth_controller import get_current_user

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_data: JobCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new job posting"""
    try:
        job_service = JobService()
        job = await job_service.create_job(job_data)
        return job
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/", response_model=List[JobResponse])
async def get_jobs(
    status: Optional[str] = Query(None, description="Filter by job status"),
    skills: Optional[str] = Query(None, description="Filter by skills (comma-separated)"),
    seniority: Optional[str] = Query(None, description="Filter by seniority level"),
    company: Optional[str] = Query(None, description="Filter by company name"),
    location: Optional[str] = Query(None, description="Filter by location"),
    type: Optional[str] = Query(None, description="Filter by job type"),
    salary_min: Optional[int] = Query(None, description="Minimum salary"),
    salary_max: Optional[int] = Query(None, description="Maximum salary"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    current_user: dict = Depends(get_current_user)
):
    """Get jobs with optional filtering"""
    # Parse skills filter
    skills_list = None
    if skills:
        skills_list = [skill.strip() for skill in skills.split(",")]
    
    # Create filter object
    filters = JobFilter(
        status=status,
        skills=skills_list,
        seniority=seniority,
        company=company,
        location=location,
        type=type,
        salary_min=salary_min,
        salary_max=salary_max
    )
    
    job_service = JobService()
    jobs = await job_service.get_jobs(filters, skip, limit)
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific job by ID"""
    job_service = JobService()
    job = await job_service.get_job_by_id(job_id)
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return job

@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: str,
    job_data: JobUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a job posting"""
    job_service = JobService()
    job = await job_service.update_job(job_id, job_data)
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return job

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a job posting"""
    job_service = JobService()
    success = await job_service.delete_job(job_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return None 