from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional, Dict, Any
from app.services.job_service import JobService
from app.schemas.job_schema import JobCreate, JobUpdate, JobResponse, JobFilter
from app.controllers.auth_controller import get_optional_user
from datetime import datetime

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
	job_data: JobCreate,
	current_user: dict = Depends(get_optional_user)
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

@router.get("/filters")
async def get_filters(current_user: dict = Depends(get_optional_user)) -> Dict[str, Any]:
	"""Return distinct values for filters (company, seniority, type, tech_skills, employment_type, status)."""
	service = JobService()
	return await service.get_distinct_filters()

@router.get("/", response_model=List[JobResponse])
async def get_jobs(
	status: Optional[str] = Query(None, description="Filter by job status"),
	skills: Optional[str] = Query(None, description="Filter by skills (comma-separated)"),
	seniority: Optional[str] = Query(None, description="Filter by seniority level"),
	company: Optional[str] = Query(None, description="Filter by company name"),
	location: Optional[str] = Query(None, description="Filter by location"),
	type: Optional[str] = Query(None, description="Filter by job type"),
	title: Optional[str] = Query(None, description="Filter by job title keyword"),
	employment_type: Optional[str] = Query(None, description="Employment type filter"),
	salary_min: Optional[int] = Query(None, description="Minimum salary"),
	salary_max: Optional[int] = Query(None, description="Maximum salary"),
	skip: int = Query(0, ge=0, description="Number of records to skip"),
	limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
	current_user: dict = Depends(get_optional_user)
):
	"""Get jobs with optional filtering; enrich with days_posted server-side."""
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
	jobs = await job_service.get_jobs(filters, skip, limit, title_keyword=title, employment_type=employment_type)
	
	# Enrich with days_posted
	for j in jobs:
		if j.posting_date:
			j.days_to_fill = (datetime.utcnow() - j.posting_date).days
	return jobs

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
	job_id: str,
	current_user: dict = Depends(get_optional_user)
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
	current_user: dict = Depends(get_optional_user)
):
	"""Update a job posting (status can be changed from frontend: new -> analyzed -> matched)."""
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
	current_user: dict = Depends(get_optional_user)
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