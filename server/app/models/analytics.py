from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema, field):
        field_schema.update(type="string")
        return field_schema

class SkillDemand(BaseModel):
    skill: str
    demand_score: float
    job_count: int
    seniority_distribution: Dict[str, int]
    avg_salary: Optional[str] = None

class SeniorityDistribution(BaseModel):
    senior: float
    mid: float
    junior: float
    total_jobs: int

class SalaryRange(BaseModel):
    min_salary: Optional[float] = None
    max_salary: Optional[float] = None
    currency: str = "USD"
    period: str = "yearly"

class SalaryByLevel(BaseModel):
    senior: str
    mid: str
    junior: str

class CompanyInsights(BaseModel):
    company: str
    total_jobs: int
    avg_salary: str
    common_skills: List[str]
    job_types: List[str]
    locations: List[str]

class DashboardStats(BaseModel):
    active_jobs: int
    new_this_week: int
    avg_process_time: str
    success_rate: float
    total_applications: int
    interviews_scheduled: int
    offers_sent: int
    hires_made: int
    last_updated: datetime

class AnalyticsData(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    top_skills: List[SkillDemand]
    seniority_distribution: SeniorityDistribution
    salary_ranges_by_level: SalaryByLevel
    company_insights: List[CompanyInsights]
    dashboard_stats: DashboardStats
    calculated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str} 