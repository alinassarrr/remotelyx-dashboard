from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    description: Optional[str] = None
    type: Optional[str] = Field(None, pattern="^(remote|hybrid|onsite)$")
    seniority: Optional[str] = Field(None, pattern="^(junior|mid|senior)$")
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    salary: Optional[str] = None
    employment_type: Optional[str] = None
    job_link: Optional[str] = None
    date_posted: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    tech_skills: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = Field(None, pattern="^(remote|hybrid|onsite)$")
    seniority: Optional[str] = Field(None, pattern="^(junior|mid|senior)$")
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    salary: Optional[str] = None
    employment_type: Optional[str] = None
    job_link: Optional[str] = None
    date_posted: Optional[str] = None
    skills: Optional[List[str]] = None
    tech_skills: Optional[List[str]] = None
    soft_skills: Optional[List[str]] = None
    status: Optional[str] = Field(None, pattern="^(new|analyzed|matched|closed)$")
    days_to_fill: Optional[int] = None
    matched_date: Optional[datetime] = None

class JobResponse(BaseModel):
    id: str
    title: str
    company: str
    location: str
    description: Optional[str] = None
    type: Optional[str] = None
    seniority: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary: Optional[str] = None
    employment_type: Optional[str] = None
    job_link: Optional[str] = None
    date_posted: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    tech_skills: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    posting_date: Optional[datetime] = None
    scraped_at: Optional[datetime] = None
    status: str
    days_to_fill: Optional[int]
    matched_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class JobFilter(BaseModel):
    status: Optional[str] = None
    skills: Optional[List[str]] = None
    seniority: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    type: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None 