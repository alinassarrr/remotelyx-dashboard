from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, validation_info=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema, field):
        field_schema.update(type="string")
        return field_schema

class JobData(BaseModel):
    company: str
    date_posted: str
    description: str
    employment_type: str
    job_link: str
    location: str
    salary: str
    scraped_at: str
    seniority: str
    soft_skills: List[str]
    tech_skills: List[str]
    title: str
    updated_at: str
    status: str = "New"  # Default status for new jobs

class ScrapedJob(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    data: JobData
    message: str
    scraped_at: str
    success: bool
    status: str = Field(default="NEW", description="Job status: NEW, ANALYZED, MATCHED")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
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
                    "tech_skills": ["React.js", "Next.js", "Node.js", "Nest.js"],
                    "title": "Full Stack Developer - IC",
                    "updated_at": "Sun, 17 Aug 2025 00:02:43 GMT"
                },
                "message": "Job updated successfully (ID: 68a11b52c7310ba19285064a)",
                "scraped_at": "2025-08-17T00:02:43.608904",
                "success": True
            }
        }

class JobInDB(ScrapedJob):
    pass

class JobCreate(ScrapedJob):
    pass

class JobUpdate(BaseModel):
    data: Optional[JobData] = None
    message: Optional[str] = None
    success: Optional[bool] = None
    status: Optional[str] = None  # Allow direct status updates
    updated_at: datetime = Field(default_factory=datetime.utcnow) 