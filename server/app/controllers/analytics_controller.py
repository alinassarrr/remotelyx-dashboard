from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics_schema import (
	AnalyticsResponse, KPIs, SkillDemand, SeniorityDistribution, 
	TrendingSkill, HardToFillRole, RecentActivity
)
from app.controllers.auth_controller import get_optional_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/", response_model=AnalyticsResponse)
async def get_full_analytics(current_user: dict = Depends(get_optional_user)):
	"""Get complete analytics data"""
	analytics_service = AnalyticsService()
	return await analytics_service.get_full_analytics()

@router.get("/kpis", response_model=KPIs)
async def get_kpis(current_user: dict = Depends(get_optional_user)):
	"""Get key performance indicators with weekly deltas"""
	analytics_service = AnalyticsService()
	return await analytics_service.get_kpis()

@router.get("/skills", response_model=list[SkillDemand])
async def get_skills_demand(
	title: Optional[str] = Query(None, description="Filter skills by job title keyword (e.g., developer)"),
	market: Optional[str] = Query("US", description="Market filter (default: US)"),
	current_user: dict = Depends(get_optional_user)
):
	"""Get skills demand analysis, optionally filtered by job title keyword and market"""
	analytics_service = AnalyticsService()
	return await analytics_service.get_skills_demand(title_keyword=title, market=market)

@router.get("/seniority", response_model=list[SeniorityDistribution])
async def get_seniority_distribution(
	title: Optional[str] = Query(None, description="Filter by job title keyword"),
	current_user: dict = Depends(get_optional_user)
):
	"""Get seniority level distribution, optionally filtered by job title keyword"""
	analytics_service = AnalyticsService()
	return await analytics_service.get_seniority_distribution(title_keyword=title)

@router.get("/trending", response_model=list[TrendingSkill])
async def get_trending_skills(
	title: Optional[str] = Query(None, description="Filter by job title keyword"),
	current_user: dict = Depends(get_optional_user)
):
	"""Get trending skills (week-over-week), optionally filtered by job title keyword"""
	analytics_service = AnalyticsService()
	return await analytics_service.get_trending_skills(title_keyword=title)

@router.get("/hard-to-fill", response_model=list[HardToFillRole])
async def get_hard_to_fill_roles(current_user: dict = Depends(get_optional_user)):
	"""Get roles that are hard to fill (high average days to fill)"""
	analytics_service = AnalyticsService()
	return await analytics_service.get_hard_to_fill_roles()

@router.get("/recent-activity", response_model=list[RecentActivity])
async def get_recent_activity(current_user: dict = Depends(get_optional_user)):
	"""Get recent activity logs"""
	analytics_service = AnalyticsService()
	return await analytics_service.get_recent_activity() 