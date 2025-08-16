from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.core.database import get_collection
from app.schemas.analytics_schema import (
    KPIs, SkillDemand, SeniorityDistribution, TrendingSkill, 
    HardToFillRole, RecentActivity, AnalyticsResponse
)

class AnalyticsService:
    def __init__(self):
        self.jobs_collection = get_collection("jobs")
        self.activity_collection = get_collection("activity_logs")

    async def get_kpis(self) -> KPIs:
        """Calculate key performance indicators"""
        # Total jobs
        total_jobs = await self.jobs_collection.count_documents({})
        
        # Active jobs (not closed)
        active_jobs = await self.jobs_collection.count_documents({"status": {"$ne": "closed"}})
        
        # New jobs this week
        week_ago = datetime.utcnow() - timedelta(days=7)
        new_this_week = await self.jobs_collection.count_documents({
            "posting_date": {"$gte": week_ago}
        })
        
        # Average processing time (matched jobs only)
        matched_jobs = await self.jobs_collection.find({"status": "matched"}).to_list(length=None)
        avg_processing_time = 0
        if matched_jobs:
            total_days = 0
            for job in matched_jobs:
                if job.get("matched_date") and job.get("posting_date"):
                    days = (job["matched_date"] - job["posting_date"]).days
                    total_days += days
            avg_processing_time = total_days / len(matched_jobs)
        
        # Success rate (matched / analyzed)
        analyzed_jobs = await self.jobs_collection.count_documents({"status": {"$in": ["analyzed", "matched"]}})
        success_rate = 0
        if analyzed_jobs > 0:
            success_rate = len(matched_jobs) / analyzed_jobs
        
        return KPIs(
            active_jobs=active_jobs,
            new_this_week=new_this_week,
            avg_processing_time=round(avg_processing_time, 2),
            success_rate=round(success_rate, 3),
            total_jobs=total_jobs
        )

    async def get_skills_demand(self) -> List[SkillDemand]:
        """Get skills demand analysis"""
        pipeline = [
            {"$unwind": "$skills"},
            {"$group": {"_id": "$skills", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 20}
        ]
        
        skills_data = await self.jobs_collection.aggregate(pipeline).to_list(length=None)
        
        # Calculate total jobs for percentage
        total_jobs = await self.jobs_collection.count_documents({})
        
        skills_demand = []
        for skill in skills_data:
            percentage = (skill["count"] / total_jobs) * 100 if total_jobs > 0 else 0
            skills_demand.append(SkillDemand(
                skill=skill["_id"],
                count=skill["count"],
                percentage=round(percentage, 2)
            ))
        
        return skills_demand

    async def get_seniority_distribution(self) -> List[SeniorityDistribution]:
        """Get seniority level distribution"""
        pipeline = [
            {"$group": {"_id": "$seniority", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        seniority_data = await self.jobs_collection.aggregate(pipeline).to_list(length=None)
        
        # Calculate total jobs for percentage
        total_jobs = await self.jobs_collection.count_documents({})
        
        seniority_dist = []
        for seniority in seniority_data:
            percentage = (seniority["count"] / total_jobs) * 100 if total_jobs > 0 else 0
            seniority_dist.append(SeniorityDistribution(
                seniority=seniority["_id"],
                count=seniority["count"],
                percentage=round(percentage, 2)
            ))
        
        return seniority_dist

    async def get_trending_skills(self) -> List[TrendingSkill]:
        """Get trending skills (comparing current week vs previous week)"""
        now = datetime.utcnow()
        current_week_start = now - timedelta(days=now.weekday())
        previous_week_start = current_week_start - timedelta(days=7)
        
        # Current week skills
        current_week_pipeline = [
            {"$match": {"posting_date": {"$gte": current_week_start}}},
            {"$unwind": "$skills"},
            {"$group": {"_id": "$skills", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        
        current_week_skills = await self.jobs_collection.aggregate(current_week_pipeline).to_list(length=None)
        
        # Previous week skills
        previous_week_pipeline = [
            {"$match": {"posting_date": {"$gte": previous_week_start, "$lt": current_week_start}}},
            {"$unwind": "$skills"},
            {"$group": {"_id": "$skills", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        
        previous_week_skills = await self.jobs_collection.aggregate(previous_week_pipeline).to_list(length=None)
        
        # Create trending skills
        trending_skills = []
        current_week_dict = {skill["_id"]: skill["count"] for skill in current_week_skills}
        previous_week_dict = {skill["_id"]: skill["count"] for skill in previous_week_skills}
        
        for skill_name in current_week_dict.keys():
            current_count = current_week_dict[skill_name]
            previous_count = previous_week_dict.get(skill_name, 0)
            
            growth_percentage = 0
            if previous_count > 0:
                growth_percentage = ((current_count - previous_count) / previous_count) * 100
            
            trending_skills.append(TrendingSkill(
                skill=skill_name,
                current_week_count=current_count,
                previous_week_count=previous_count,
                growth_percentage=round(growth_percentage, 2)
            ))
        
        # Sort by growth percentage
        trending_skills.sort(key=lambda x: x.growth_percentage, reverse=True)
        return trending_skills[:10]

    async def get_hard_to_fill_roles(self) -> List[HardToFillRole]:
        """Get roles that are hard to fill (high average days to fill)"""
        pipeline = [
            {"$match": {"days_to_fill": {"$exists": True, "$ne": None}}},
            {"$group": {"_id": "$title", "avg_days_to_fill": {"$avg": "$days_to_fill"}, "job_count": {"$sum": 1}}},
            {"$match": {"job_count": {"$gte": 3}}},  # Only roles with at least 3 jobs
            {"$sort": {"avg_days_to_fill": -1}},
            {"$limit": 10}
        ]
        
        hard_to_fill_data = await self.jobs_collection.aggregate(pipeline).to_list(length=None)
        
        hard_to_fill_roles = []
        for role in hard_to_fill_data:
            hard_to_fill_roles.append(HardToFillRole(
                title=role["_id"],
                avg_days_to_fill=round(role["avg_days_to_fill"], 1),
                job_count=role["job_count"]
            ))
        
        return hard_to_fill_roles

    async def get_recent_activity(self, limit: int = 20) -> List[RecentActivity]:
        """Get recent activity logs"""
        cursor = self.activity_collection.find().sort("timestamp", -1).limit(limit)
        
        recent_activity = []
        async for activity in cursor:
            recent_activity.append(RecentActivity(
                event=activity["event"],
                timestamp=activity["timestamp"],
                details=activity.get("details", {})
            ))
        
        return recent_activity

    async def get_full_analytics(self) -> AnalyticsResponse:
        """Get complete analytics data"""
        kpis = await self.get_kpis()
        skills_demand = await self.get_skills_demand()
        seniority_distribution = await self.get_seniority_distribution()
        trending_skills = await self.get_trending_skills()
        hard_to_fill_roles = await self.get_hard_to_fill_roles()
        recent_activity = await self.get_recent_activity()
        
        return AnalyticsResponse(
            kpis=kpis,
            skills_demand=skills_demand,
            seniority_distribution=seniority_distribution,
            trending_skills=trending_skills,
            hard_to_fill_roles=hard_to_fill_roles,
            recent_activity=recent_activity
        ) 