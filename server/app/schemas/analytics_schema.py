from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

class KPIs(BaseModel):
    active_jobs: int
    new_this_week: int
    avg_processing_time: float
    success_rate: float
    total_jobs: int

class SkillDemand(BaseModel):
    skill: str
    count: int
    percentage: float

class SeniorityDistribution(BaseModel):
    seniority: str
    count: int
    percentage: float

class TrendingSkill(BaseModel):
    skill: str
    current_week_count: int
    previous_week_count: int
    growth_percentage: float

class HardToFillRole(BaseModel):
    title: str
    avg_days_to_fill: float
    job_count: int

class RecentActivity(BaseModel):
    event: str
    timestamp: datetime
    details: Dict[str, Any]

class AnalyticsResponse(BaseModel):
    kpis: KPIs
    skills_demand: List[SkillDemand]
    seniority_distribution: List[SeniorityDistribution]
    trending_skills: List[TrendingSkill]
    hard_to_fill_roles: List[HardToFillRole]
    recent_activity: List[RecentActivity] 