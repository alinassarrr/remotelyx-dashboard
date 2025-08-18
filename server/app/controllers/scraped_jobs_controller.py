from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from datetime import datetime
import logging

from app.schemas.scraped_job_schema import (
    BulkScrapedJobsRequest, 
    BulkImportResponse, 
    ScrapedJobResponse
)
from app.models.job_model import JobModel
from app.services.job_service import JobService
from app.utils.database import get_database

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/scraped-jobs", tags=["Scraped Jobs"])

@router.post("/import", response_model=BulkImportResponse)
async def import_scraped_jobs(
    request: BulkScrapedJobsRequest,
    db=Depends(get_database)
):
    """
    Import jobs from scraper data.
    Handles bulk import with duplicate detection and error handling.
    """
    job_service = JobService(db)
    
    total_jobs = len(request.jobs)
    successful_imports = 0
    failed_imports = 0
    created_jobs = []
    updated_jobs = []
    errors = []
    
    logger.info(f"Starting import of {total_jobs} scraped jobs")
    
    for idx, scraped_job in enumerate(request.jobs):
        try:
            if not scraped_job.success:
                errors.append(f"Job {idx + 1}: Scraper marked as unsuccessful - {scraped_job.message}")
                failed_imports += 1
                continue
            
            # Convert scraped data to job model format
            job_data = scraped_job.data.to_job_model_dict()
            
            # Check for existing job by company, title, and job_link
            existing_job = await job_service.find_duplicate_job(
                company=scraped_job.data.company,
                title=scraped_job.data.title,
                job_link=scraped_job.data.job_link
            )
            
            if existing_job:
                # Update existing job with new scraped data
                job_data["updated_at"] = datetime.utcnow()
                updated_job = await job_service.update_job(
                    str(existing_job.id), 
                    job_data
                )
                updated_jobs.append(str(existing_job.id))
                logger.info(f"Updated existing job: {scraped_job.data.title} at {scraped_job.data.company}")
            else:
                # Create new job
                new_job = JobModel(**job_data)
                created_job = await job_service.create_job_from_model(new_job)
                created_jobs.append(str(created_job.id))
                logger.info(f"Created new job: {scraped_job.data.title} at {scraped_job.data.company}")
            
            successful_imports += 1
            
        except Exception as e:
            error_msg = f"Job {idx + 1} ({scraped_job.data.title} at {scraped_job.data.company}): {str(e)}"
            errors.append(error_msg)
            failed_imports += 1
            logger.error(f"Failed to import job: {error_msg}")
    
    # Generate summary message
    if successful_imports == total_jobs:
        message = f"Successfully imported all {total_jobs} jobs"
    elif successful_imports > 0:
        message = f"Imported {successful_imports} of {total_jobs} jobs with {failed_imports} failures"
    else:
        message = f"Failed to import any jobs. {failed_imports} failures"
    
    logger.info(f"Import completed: {successful_imports} successful, {failed_imports} failed")
    
    return BulkImportResponse(
        total_jobs=total_jobs,
        successful_imports=successful_imports,
        failed_imports=failed_imports,
        created_jobs=created_jobs,
        updated_jobs=updated_jobs,
        errors=errors,
        message=message
    )


@router.post("/import/single", response_model=dict)
async def import_single_scraped_job(
    scraped_job: ScrapedJobResponse,
    db=Depends(get_database)
):
    """
    Import a single job from scraper data.
    """
    if not scraped_job.success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Scraper marked job as unsuccessful: {scraped_job.message}"
        )
    
    job_service = JobService(db)
    
    try:
        # Convert scraped data to job model format
        job_data = scraped_job.data.to_job_model_dict()
        
        # Check for existing job
        existing_job = await job_service.find_duplicate_job(
            company=scraped_job.data.company,
            title=scraped_job.data.title,
            job_link=scraped_job.data.job_link
        )
        
        if existing_job:
            # Update existing job
            job_data["updated_at"] = datetime.utcnow()
            updated_job = await job_service.update_job(
                str(existing_job.id), 
                job_data
            )
            return {
                "action": "updated",
                "job_id": str(existing_job.id),
                "message": f"Updated existing job: {scraped_job.data.title}"
            }
        else:
            # Create new job
            new_job = JobModel(**job_data)
            created_job = await job_service.create_job_from_model(new_job)
            return {
                "action": "created",
                "job_id": str(created_job.id),
                "message": f"Created new job: {scraped_job.data.title}"
            }
            
    except Exception as e:
        logger.error(f"Failed to import job {scraped_job.data.title}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to import job: {str(e)}"
        )


@router.get("/stats")
async def get_scraped_jobs_stats(db=Depends(get_database)):
    """
    Get statistics about scraped jobs.
    """
    job_service = JobService(db)
    
    try:
        # Get counts of scraped vs non-scraped jobs
        total_jobs = await job_service.count_jobs()
        scraped_jobs = await job_service.count_jobs_with_scraped_data()
        
        # Get recent scraping activity
        recent_scraped = await job_service.get_recently_scraped_jobs(days=7)
        
        return {
            "total_jobs": total_jobs,
            "scraped_jobs": scraped_jobs,
            "manual_jobs": total_jobs - scraped_jobs,
            "recently_scraped": len(recent_scraped),
            "scraping_coverage": round((scraped_jobs / total_jobs * 100), 2) if total_jobs > 0 else 0
        }
        
    except Exception as e:
        logger.error(f"Failed to get scraping stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get scraping statistics: {str(e)}"
        ) 