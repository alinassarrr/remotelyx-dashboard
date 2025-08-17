from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
import re

class ScrapedJobData(BaseModel):
    """Schema for job data coming from the scraper"""
    company: str
    date_posted: str
    description: str
    employment_type: str
    job_link: str
    location: str
    salary: str
    scraped_at: str  # Will be converted to datetime
    seniority: str
    soft_skills: List[str] = Field(default_factory=list)
    tech_skills: List[str] = Field(default_factory=list)
    title: str
    updated_at: str  # Will be converted to datetime

    @validator('scraped_at', 'updated_at', pre=True)
    def parse_datetime_string(cls, v):
        """Convert datetime strings to datetime objects"""
        if isinstance(v, str):
            try:
                # Handle format: "Sun, 17 Aug 2025 00:02:43 GMT"
                return datetime.strptime(v, "%a, %d %b %Y %H:%M:%S %Z")
            except ValueError:
                try:
                    # Handle ISO format: "2025-08-17T00:02:43.608904"
                    return datetime.fromisoformat(v.replace('Z', '+00:00'))
                except ValueError:
                    # Fallback to current time if parsing fails
                    return datetime.utcnow()
        return v

    @validator('seniority')
    def normalize_seniority(cls, v):
        """Normalize seniority to match our enum"""
        if v.lower() in ['mid', 'middle']:
            return 'mid'
        elif v.lower() in ['senior', 'sr']:
            return 'senior'
        elif v.lower() in ['junior', 'jr', 'entry']:
            return 'junior'
        return 'mid'  # Default fallback

    def extract_salary_range(self) -> tuple[Optional[int], Optional[int]]:
        """Extract numeric salary range from salary string"""
        if not self.salary or self.salary.lower() in ['not specified', 'competitive']:
            return None, None
        
        # Extract numbers from salary string
        numbers = re.findall(r'[\d,]+', self.salary.replace(',', ''))
        if numbers:
            try:
                # Convert first number found
                salary_num = int(numbers[0])
                # If it's likely monthly, return as min and estimate max
                if salary_num < 10000:  # Likely monthly
                    return salary_num, salary_num * 2
                else:  # Likely annual
                    return salary_num, salary_num + 20000
            except ValueError:
                pass
        return None, None

    def to_job_model_dict(self) -> dict:
        """Convert scraped data to JobModel format"""
        salary_min, salary_max = self.extract_salary_range()
        
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "description": self.description,
            "employment_type": self.employment_type,
            "job_link": self.job_link,
            "salary": self.salary,
            "date_posted": self.date_posted,
            "tech_skills": self.tech_skills,
            "soft_skills": self.soft_skills,
            "seniority": self.seniority,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "scraped_at": self.scraped_at,
            "posting_date": self.scraped_at,  # Use scraped_at as posting_date
            "status": "new",
            # Type inferred from location in the model validator
        }


class ScrapedJobResponse(BaseModel):
    """Schema for the response from scraper"""
    data: ScrapedJobData
    message: str
    scraped_at: str
    success: bool

    @validator('scraped_at', pre=True)
    def parse_scraped_at(cls, v):
        """Parse the top-level scraped_at timestamp"""
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                return datetime.utcnow()
        return v


class BulkScrapedJobsRequest(BaseModel):
    """Schema for bulk job import from scraper"""
    jobs: List[ScrapedJobResponse]
    
    class Config:
        json_schema_extra = {
            "example": {
                "jobs": [
                    {
                        "data": {
                            "company": "Gamma",
                            "date_posted": "Not specified",
                            "description": "We are looking for a highly skilled Full-Stack Developer...",
                            "employment_type": "Full-time",
                            "job_link": "https://gamma.app/docs/full-stack-developer...",
                            "location": "Remote",
                            "salary": "$2,500+",
                            "scraped_at": "Sun, 17 Aug 2025 00:02:43 GMT",
                            "seniority": "Mid",
                            "soft_skills": ["communication", "leadership", "teamwork", "problem-solving"],
                            "tech_skills": ["React.js", "Next.js", "Node.js", "Nest.js", "MySQL"],
                            "title": "Full Stack Developer - IC",
                            "updated_at": "Sun, 17 Aug 2025 00:02:43 GMT"
                        },
                        "message": "Job updated successfully (ID: 68a11b52c7310ba19285064a)",
                        "scraped_at": "2025-08-17T00:02:43.608904",
                        "success": True
                    }
                ]
            }
        }


class BulkImportResponse(BaseModel):
    """Response schema for bulk job import"""
    total_jobs: int
    successful_imports: int
    failed_imports: int
    created_jobs: List[str] = Field(default_factory=list)
    updated_jobs: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    message: str 