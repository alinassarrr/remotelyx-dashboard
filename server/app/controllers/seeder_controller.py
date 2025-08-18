from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from app.services.seeder_service import SeederService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/seeder", tags=["seeder"])

# Dependency to get seeder service
def get_seeder_service():
    return SeederService()

@router.post("/seed/sample", response_model=dict)
async def seed_sample_jobs(
    count: int = Query(50, ge=1, le=1000, description="Number of sample jobs to create"),
    seeder_service: SeederService = Depends(get_seeder_service)
):
    """Seed the database with sample job data for development/testing."""
    try:
        job_ids = await seeder_service.seed_sample_jobs(count)
        return {
            "message": f"Successfully seeded {len(job_ids)} sample jobs",
            "job_ids": job_ids,
            "count": len(job_ids)
        }
    except Exception as e:
        logger.error(f"Error seeding sample jobs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to seed sample jobs: {str(e)}")

@router.post("/seed/n8n", response_model=dict)
async def seed_n8n_format_jobs(
    jobs_data: List[dict],
    seeder_service: SeederService = Depends(get_seeder_service)
):
    """Seed jobs from n8n scraper format."""
    try:
        if not jobs_data:
            raise HTTPException(status_code=400, detail="No job data provided")
        
        job_ids = await seeder_service.seed_n8n_format_jobs(jobs_data)
        return {
            "message": f"Successfully seeded {len(job_ids)} jobs from n8n format",
            "job_ids": job_ids,
            "count": len(job_ids),
            "input_count": len(jobs_data)
        }
    except Exception as e:
        logger.error(f"Error seeding n8n format jobs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to seed n8n format jobs: {str(e)}")

@router.delete("/clear", response_model=dict)
async def clear_all_jobs(
    seeder_service: SeederService = Depends(get_seeder_service)
):
    """Clear all jobs from the database."""
    try:
        success = await seeder_service.clear_all_jobs()
        if success:
            return {
                "message": "All jobs cleared successfully",
                "status": "cleared"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to clear jobs")
    except Exception as e:
        logger.error(f"Error clearing jobs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to clear jobs: {str(e)}")

@router.get("/status", response_model=dict)
async def get_seeding_status(
    seeder_service: SeederService = Depends(get_seeder_service)
):
    """Get the current status of the database."""
    try:
        status = await seeder_service.get_seeding_status()
        return status
    except Exception as e:
        logger.error(f"Error getting seeding status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get seeding status: {str(e)}")

@router.post("/seed/example-n8n", response_model=dict)
async def seed_example_n8n_data(
    seeder_service: SeederService = Depends(get_seeder_service)
):
    """Seed the database with the example n8n format data provided in the requirements."""
    try:
        # Example n8n format data from requirements
        example_jobs = [
            {
                "data": {
                    "company": "Gamma",
                    "date_posted": "Not specified",
                    "description": "We are looking for a highly skilled Full-Stack Developer with 3+ years of experience to join our dynamic team and help build an AI SaaS platform in the ALCOHOLIC BEVERAGE niche. Develop and maintain full-stack web applications using React.js/Next.js (Frontend), Node.js/ Nest.js (Backend). Design and manage databases using MySQL and Vector Databases for optimized performance. Develop and integrate APIs to connect various services and applications. Work with AI tools to enhance application features, including AI-driven automation, chatbots, and data processing. Deploy and manage applications on AWS, ensuring scalability, security, and high availability. Optimize front-end performance, ensuring smooth UI/UX experiences. Implement authentication and security best practices, including OAuth, JWT, and data encryption. Work with DevOps tools for CI/CD, containerization (Docker), and server management. Troubleshoot and debug application issues, ensuring high performance and reliability.",
                    "employment_type": "Full-time",
                    "job_link": "https://gamma.app/docs/full-stack-developer-ic-3s64m1oqf3nuf5u?mode=doc.",
                    "location": "Remote",
                    "salary": "$2,500+",
                    "scraped_at": "Sun, 17 Aug 2025 00:02:43 GMT",
                    "seniority": "Mid",
                    "soft_skills": [
                        "communication",
                        "leadership",
                        "teamwork",
                        "problem-solving"
                    ],
                    "tech_skills": [
                        "React.js",
                        "Next.js",
                        "Node.js",
                        "Nest.js",
                        "MySQL",
                        "PostgreSQL",
                        "Vector DB",
                        "AWS",
                        "Docker",
                        "CI/CD Pipelines",
                        "OpenAI APIs",
                        "LangChain",
                        "GraphQL"
                    ],
                    "title": "Full Stack Developer - IC",
                    "updated_at": "Sun, 17 Aug 2025 00:02:43 GMT"
                },
                "message": "Job updated successfully (ID: 68a11b52c7310ba19285064a)",
                "scraped_at": "2025-08-17T00:02:43.608904",
                "success": True
            }
        ]
        
        job_ids = await seeder_service.seed_n8n_format_jobs(example_jobs)
        return {
            "message": f"Successfully seeded {len(job_ids)} example n8n format jobs",
            "job_ids": job_ids,
            "count": len(job_ids)
        }
    except Exception as e:
        logger.error(f"Error seeding example n8n data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to seed example n8n data: {str(e)}") 