from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from app.services.analytics_service import AnalyticsService
from app.models.analytics import AnalyticsData, DashboardStats
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["analytics"])

# Dependency to get analytics service
def get_analytics_service():
    return AnalyticsService()

@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """Get real-time dashboard statistics."""
    try:
        stats = await analytics_service.calculate_dashboard_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting dashboard stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve dashboard statistics")

@router.get("/skills/top", response_model=dict)
async def get_top_skills(
    role: Optional[str] = Query(None, description="Filter skills by role"),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """Get top skills in demand with optional role filtering."""
    try:
        top_skills = await analytics_service.calculate_top_skills()
        
        # If role is specified, filter skills by role
        if role and role.lower() != "all":
            skills_by_role = await analytics_service.get_skills_by_role()
            role_skills = skills_by_role.get(role, [])
            if role_skills:
                # Filter top skills to only include skills relevant to the role
                filtered_skills = [skill for skill in top_skills if skill.skill in role_skills]
                top_skills = filtered_skills[:8]  # Limit to top 8 for the role
        
        return {
            "skills": top_skills,
            "total_skills": len(top_skills),
            "role_filter": role
        }
    except Exception as e:
        logger.error(f"Error getting top skills: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve top skills")

@router.get("/seniority/distribution", response_model=dict)
async def get_seniority_distribution(
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """Get seniority level distribution across all jobs."""
    try:
        seniority_dist = await analytics_service.calculate_seniority_distribution()
        return {
            "distribution": seniority_dist,
            "total_jobs": seniority_dist.total_jobs
        }
    except Exception as e:
        logger.error(f"Error getting seniority distribution: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve seniority distribution")

@router.get("/salary/ranges", response_model=dict)
async def get_salary_ranges_by_level(
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """Get average salary ranges by seniority level."""
    try:
        salary_ranges = await analytics_service.calculate_salary_ranges_by_level()
        return {
            "salary_ranges": salary_ranges,
            "currency": "USD",
            "period": "yearly"
        }
    except Exception as e:
        logger.error(f"Error getting salary ranges: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve salary ranges")

@router.get("/companies/insights", response_model=dict)
async def get_company_insights(
    limit: int = Query(10, ge=1, le=50, description="Maximum number of companies to return"),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """Get insights about companies and their job postings."""
    try:
        company_insights = await analytics_service.calculate_company_insights(limit)
        return {
            "companies": company_insights,
            "total_companies": len(company_insights),
            "limit": limit
        }
    except Exception as e:
        logger.error(f"Error getting company insights: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve company insights")

@router.get("/skills/by-role", response_model=dict)
async def get_skills_by_role(
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """Get skills mapped to different roles for filtering."""
    try:
        skills_by_role = await analytics_service.get_skills_by_role()
        return {
            "skills_by_role": skills_by_role,
            "available_roles": list(skills_by_role.keys())
        }
    except Exception as e:
        logger.error(f"Error getting skills by role: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve skills by role")

@router.get("/full", response_model=AnalyticsData)
async def get_full_analytics(
    force_refresh: bool = Query(False, description="Force refresh of analytics data"),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """Get complete analytics data for the dashboard."""
    try:
        if not force_refresh:
            # Try to get cached analytics first
            cached_analytics = await analytics_service.get_cached_analytics()
            if cached_analytics:
                return cached_analytics
        
        # Generate fresh analytics
        analytics_data = await analytics_service.generate_full_analytics()
        return analytics_data
        
    except Exception as e:
        logger.error(f"Error getting full analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics data")

@router.post("/refresh", response_model=dict)
async def refresh_analytics(
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """Force refresh of all analytics data."""
    try:
        analytics_data = await analytics_service.generate_full_analytics()
        return {
            "message": "Analytics refreshed successfully",
            "calculated_at": analytics_data.calculated_at,
            "analytics_id": str(analytics_data.id)
        }
    except Exception as e:
        logger.error(f"Error refreshing analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to refresh analytics")

@router.get("/overview", response_model=dict)
async def get_analytics_overview(
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """Get a quick overview of key analytics metrics."""
    try:
        # Get basic stats
        dashboard_stats = await analytics_service.calculate_dashboard_stats()
        
        # Get top 5 skills
        top_skills = await analytics_service.calculate_top_skills()
        top_5_skills = top_skills[:5] if top_skills else []
        
        # Get seniority distribution
        seniority_dist = await analytics_service.calculate_seniority_distribution()
        
        return {
            "dashboard_stats": dashboard_stats,
            "top_5_skills": top_5_skills,
            "seniority_distribution": seniority_dist,
            "last_updated": dashboard_stats.last_updated
        }
        
    except Exception as e:
        logger.error(f"Error getting analytics overview: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics overview")

@router.get("/trends/weekly", response_model=dict)
async def get_weekly_trends(
    weeks: int = Query(4, ge=1, le=12, description="Number of weeks to analyze"),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    """Get weekly trends for key metrics."""
    try:
        # This would be a more sophisticated calculation in a real system
        # For now, we'll return mock trend data
        from datetime import datetime, timedelta
        
        trends = []
        for i in range(weeks):
            week_start = datetime.utcnow() - timedelta(weeks=i+1)
            week_end = week_start + timedelta(days=7)
            
            # Mock trend data (would be calculated from actual historical data)
            trends.append({
                "week_start": week_start.isoformat(),
                "week_end": week_end.isoformat(),
                "new_jobs": max(10, 50 - (i * 5)),  # Decreasing trend
                "active_jobs": max(100, 500 - (i * 20)),
                "top_skill": "Python" if i % 2 == 0 else "JavaScript",
                "avg_salary": "$75-95k"
            })
        
        return {
            "trends": trends,
            "weeks_analyzed": weeks,
            "analysis_date": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting weekly trends: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve weekly trends") 