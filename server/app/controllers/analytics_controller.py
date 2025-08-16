from fastapi import APIRouter, Depends
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics_schema import (
    AnalyticsResponse, KPIs, SkillDemand, SeniorityDistribution, 
    TrendingSkill, HardToFillRole, RecentActivity
)
from app.controllers.auth_controller import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/", response_model=AnalyticsResponse)
async def get_full_analytics(current_user: dict = Depends(get_current_user)):
    """Get complete analytics data"""
    analytics_service = AnalyticsService()
    return await analytics_service.get_full_analytics()

@router.get("/kpis", response_model=KPIs)
async def get_kpis(current_user: dict = Depends(get_current_user)):
    """Get key performance indicators"""
    analytics_service = AnalyticsService()
    return await analytics_service.get_kpis()

@router.get("/skills", response_model=list[SkillDemand])
async def get_skills_demand(current_user: dict = Depends(get_current_user)):
    """Get skills demand analysis"""
    analytics_service = AnalyticsService()
    return await analytics_service.get_skills_demand()

@router.get("/seniority", response_model=list[SeniorityDistribution])
async def get_seniority_distribution(current_user: dict = Depends(get_current_user)):
    """Get seniority level distribution"""
    analytics_service = AnalyticsService()
    return await analytics_service.get_seniority_distribution()

@router.get("/trending", response_model=list[TrendingSkill])
async def get_trending_skills(current_user: dict = Depends(get_current_user)):
    """Get trending skills (comparing current week vs previous week)"""
    analytics_service = AnalyticsService()
    return await analytics_service.get_trending_skills()

@router.get("/hard-to-fill", response_model=list[HardToFillRole])
async def get_hard_to_fill_roles(current_user: dict = Depends(get_current_user)):
    """Get roles that are hard to fill (high average days to fill)"""
    analytics_service = AnalyticsService()
    return await analytics_service.get_hard_to_fill_roles()

@router.get("/recent-activity", response_model=list[RecentActivity])
async def get_recent_activity(current_user: dict = Depends(get_current_user)):
    """Get recent activity logs"""
    analytics_service = AnalyticsService()
    return await analytics_service.get_recent_activity() 