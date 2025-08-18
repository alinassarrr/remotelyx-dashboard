from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from bson import ObjectId
from app.models.user_model import PyObjectId

class JobModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(..., index=True)
    company: str = Field(..., index=True)
    location: str = Field(..., index=True)
    description: Optional[str] = Field(None, description="Full job description")
    
    # Original fields with backward compatibility
    type: Optional[str] = Field(None, pattern="^(remote|hybrid|onsite)$")
    seniority: Optional[str] = Field(None, pattern="^(junior|mid|senior)$")
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    skills: List[str] = Field(default_factory=list, index=True)
    
    # New fields for scraped data
    employment_type: Optional[str] = Field(None, description="e.g., Full-time, Part-time, Contract")
    job_link: Optional[str] = Field(None, description="Original job posting URL")
    salary: Optional[str] = Field(None, description="Salary as text (e.g., '$2,500+', 'Competitive')")
    date_posted: Optional[str] = Field(None, description="Original posting date from scraper")
    
    # Separate skill categories
    tech_skills: List[str] = Field(default_factory=list, index=True, description="Technical skills")
    soft_skills: List[str] = Field(default_factory=list, description="Soft skills")
    
    # Timestamps
    posting_date: Optional[datetime] = Field(None, description="Parsed posting date")
    scraped_at: Optional[datetime] = Field(None, description="When job was scraped")
    
    # Status and tracking
    status: str = Field(default="new", pattern="^(new|analyzed|matched|closed)$")
    days_to_fill: Optional[int] = None
    matched_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator('skills', always=True)
    def combine_skills(cls, v, values):
        """Combine tech_skills and soft_skills into skills for backward compatibility"""
        tech_skills = values.get('tech_skills', [])
        soft_skills = values.get('soft_skills', [])
        return list(set(v + tech_skills + soft_skills))

    @validator('seniority', always=True)
    def normalize_seniority(cls, v):
        """Normalize seniority levels"""
        if v and v.lower() == 'mid':
            return 'mid'
        elif v and v.lower() in ['senior', 'sr']:
            return 'senior'
        elif v and v.lower() in ['junior', 'jr', 'entry']:
            return 'junior'
        return v

    @validator('type', always=True)
    def normalize_location_type(cls, v, values):
        """Infer type from location if not provided"""
        if v:
            return v
        location = values.get('location', '').lower()
        if 'remote' in location:
            return 'remote'
        elif 'hybrid' in location:
            return 'hybrid'
        else:
            return 'onsite'

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "title": "Full Stack Developer - IC",
                "company": "Gamma",
                "location": "Remote",
                "description": "We are looking for a highly skilled Full-Stack Developer...",
                "employment_type": "Full-time",
                "job_link": "https://gamma.app/docs/full-stack-developer...",
                "salary": "$2,500+",
                "date_posted": "Not specified",
                "tech_skills": ["React.js", "Next.js", "Node.js", "Nest.js"],
                "soft_skills": ["communication", "leadership", "teamwork"],
                "type": "remote",
                "seniority": "mid",
                "salary_min": 2500,
                "salary_max": 5000,
                "scraped_at": "2025-08-17T00:02:43.608904",
                "status": "new"
            }
        }
    } 