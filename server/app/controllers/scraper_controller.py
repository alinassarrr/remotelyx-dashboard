"""
Job Scraper API Controller
REST API endpoints for job scraping functionality
"""
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from ..services.scraper_service import JobScraperService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/scraper", tags=["scraper"])

# Request/Response models
class ScrapeRequest(BaseModel):
    job_url: str

class ScrapeResponse(BaseModel):
    success: bool
    data: Dict[str, Any] = None
    message: str

@router.get("/health")
async def health_check():
    """Health check endpoint for scraper service"""
    try:
        scraper_service = JobScraperService()
        stats = await scraper_service.get_job_stats()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": {
                "connected": True,
                "total_jobs": stats.get("total_jobs", 0),
                "jobs_today": stats.get("jobs_today", 0)
            },
            "extraction": {
                "method": "intelligent_keyword_based",
                "features": ["skills_detection", "salary_extraction", "gamma_app_optimized"]
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@router.post("/scrape", response_model=ScrapeResponse)
async def scrape_job(request: ScrapeRequest):
    """
    Scrape job data from URL and save to database
    """
    try:
        if not request.job_url or not request.job_url.startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="Valid job URL is required")
        
        scraper_service = JobScraperService()
        job_data = await scraper_service.scrape_and_save_job(request.job_url)
        
        return ScrapeResponse(
            success=True,
            data=job_data,
            message="Job scraped and saved successfully"
        )
        
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to scrape job data")

@router.get("/jobs")
async def get_recent_jobs(limit: int = 10, skip: int = 0):
    """
    Get recent jobs from database
    """
    try:
        scraper_service = JobScraperService()
        jobs = await scraper_service.get_recent_jobs(limit=limit, skip=skip)
        
        return {
            "success": True,
            "data": jobs,
            "count": len(jobs),
            "pagination": {
                "limit": limit,
                "skip": skip
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch jobs: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch jobs")

@router.get("/stats")
async def get_scraper_stats():
    """
    Get scraper statistics
    """
    try:
        scraper_service = JobScraperService()
        stats = await scraper_service.get_job_stats()
        
        return {
            "success": True,
            "data": stats
        }
        
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")
