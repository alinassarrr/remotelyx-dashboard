from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorCollection
from app.core.database import get_collection, JOBS_COLLECTION, ANALYTICS_COLLECTION
from app.models.analytics import (
    AnalyticsData, SkillDemand, SeniorityDistribution, 
    SalaryByLevel, CompanyInsights, DashboardStats
)
from app.models.job import ScrapedJob
import logging
import re

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self):
        self.jobs_collection: AsyncIOMotorCollection = get_collection(JOBS_COLLECTION)
        self.analytics_collection: AsyncIOMotorCollection = get_collection(ANALYTICS_COLLECTION)
    
    async def calculate_dashboard_stats(self) -> DashboardStats:
        """Calculate real-time dashboard statistics."""
        try:
            # Total active jobs
            total_jobs = await self.jobs_collection.count_documents({})
            
            # Jobs created this week
            week_ago = datetime.utcnow() - timedelta(days=7)
            new_this_week = await self.jobs_collection.count_documents({
                "created_at": {"$gte": week_ago}
            })
            
            # Mock data for now (these would come from actual application tracking)
            # In a real system, you'd have separate collections for applications, interviews, etc.
            total_applications = int(total_jobs * 1.4)  # Mock: 1.4 applications per job
            interviews_scheduled = int(total_applications * 0.125)  # Mock: 12.5% interview rate
            offers_sent = int(interviews_scheduled * 0.57)  # Mock: 57% offer rate
            hires_made = int(offers_sent * 0.75)  # Mock: 75% acceptance rate
            
            # Calculate success rate (mock: based on job fill rate)
            success_rate = min(95.0, max(85.0, (hires_made / max(total_jobs, 1)) * 100))
            
            # Mock processing time (would be calculated from actual data)
            avg_process_time = "3.2 days"
            
            return DashboardStats(
                active_jobs=total_jobs,
                new_this_week=new_this_week,
                avg_process_time=avg_process_time,
                success_rate=round(success_rate, 1),
                total_applications=total_applications,
                interviews_scheduled=interviews_scheduled,
                offers_sent=offers_sent,
                hires_made=hires_made,
                last_updated=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error calculating dashboard stats: {e}")
            raise e
    
    async def calculate_top_skills(self) -> List[SkillDemand]:
        """Calculate top skills in demand with scoring."""
        try:
            # Aggregate skills from all jobs
            pipeline = [
                {"$unwind": "$data.tech_skills"},
                {"$group": {
                    "_id": "$data.tech_skills",
                    "job_count": {"$sum": 1},
                    "seniority_dist": {
                        "$push": "$data.seniority"
                    }
                }},
                {"$sort": {"job_count": -1}},
                {"$limit": 20}
            ]
            
            skills_data = await self.jobs_collection.aggregate(pipeline).to_list(None)
            
            top_skills = []
            for skill_data in skills_data:
                skill_name = skill_data["_id"]
                job_count = skill_data["job_count"]
                
                # Calculate seniority distribution for this skill
                seniority_dist = {}
                for level in skill_data["seniority_dist"]:
                    level_lower = level.lower()
                    if "senior" in level_lower or "lead" in level_lower:
                        seniority_dist["senior"] = seniority_dist.get("senior", 0) + 1
                    elif "mid" in level_lower:
                        seniority_dist["mid"] = seniority_dist.get("mid", 0) + 1
                    else:
                        seniority_dist["junior"] = seniority_dist.get("junior", 0) + 1
                
                # Calculate demand score (0-100)
                # Base score on job count, normalized to top skill
                max_jobs = skills_data[0]["job_count"] if skills_data else 1
                demand_score = (job_count / max_jobs) * 100
                
                # Boost score for skills that appear across multiple seniority levels
                seniority_bonus = min(10, len(seniority_dist) * 2)
                demand_score = min(100, demand_score + seniority_bonus)
                
                top_skills.append(SkillDemand(
                    skill=skill_name,
                    demand_score=round(demand_score, 1),
                    job_count=job_count,
                    seniority_distribution=seniority_dist
                ))
            
            return top_skills
            
        except Exception as e:
            logger.error(f"Error calculating top skills: {e}")
            raise e
    
    async def calculate_seniority_distribution(self) -> SeniorityDistribution:
        """Calculate seniority level distribution across all jobs."""
        try:
            pipeline = [
                {"$group": {
                    "_id": "$data.seniority",
                    "count": {"$sum": 1}
                }},
                {"$sort": {"count": -1}}
            ]
            
            seniority_data = await self.jobs_collection.aggregate(pipeline).to_list(None)
            
            total_jobs = sum(item["count"] for item in seniority_data)
            if total_jobs == 0:
                return SeniorityDistribution(senior=0, mid=0, junior=0, total_jobs=0)
            
            # Initialize counters
            senior_count = 0
            mid_count = 0
            junior_count = 0
            
            # Categorize seniority levels
            for item in seniority_data:
                level = item["_id"].lower()
                count = item["count"]
                
                if "senior" in level or "lead" in level or "executive" in level:
                    senior_count += count
                elif "mid" in level or "middle" in level:
                    mid_count += count
                else:
                    junior_count += count
            
            # Calculate percentages
            senior_pct = (senior_count / total_jobs) * 100
            mid_pct = (mid_count / total_jobs) * 100
            junior_pct = (junior_count / total_jobs) * 100
            
            return SeniorityDistribution(
                senior=round(senior_pct, 1),
                mid=round(mid_pct, 1),
                junior=round(junior_pct, 1),
                total_jobs=total_jobs
            )
            
        except Exception as e:
            logger.error(f"Error calculating seniority distribution: {e}")
            raise e
    
    async def calculate_salary_ranges_by_level(self) -> SalaryByLevel:
        """Calculate average salary ranges by seniority level."""
        try:
            # This is a simplified calculation - in reality you'd parse salary strings
            # and calculate actual ranges. For now, we'll use mock data based on job counts.
            
            # Get job counts by seniority
            pipeline = [
                {"$group": {
                    "_id": "$data.seniority",
                    "count": {"$sum": 1}
                }}
            ]
            
            seniority_counts = await self.jobs_collection.aggregate(pipeline).to_list(None)
            
            # Mock salary ranges based on seniority distribution
            # In a real system, you'd parse actual salary data
            senior_salary = "$85-120k"
            mid_salary = "$60-85k"
            junior_salary = "$40-60k"
            
            return SalaryByLevel(
                senior=senior_salary,
                mid=mid_salary,
                junior=junior_salary
            )
            
        except Exception as e:
            logger.error(f"Error calculating salary ranges: {e}")
            raise e
    
    async def calculate_company_insights(self, limit: int = 10) -> List[CompanyInsights]:
        """Calculate insights about companies and their job postings."""
        try:
            pipeline = [
                {"$group": {
                    "_id": "$data.company",
                    "total_jobs": {"$sum": 1},
                    "job_types": {"$addToSet": "$data.employment_type"},
                    "locations": {"$addToSet": "$data.location"},
                    "all_skills": {"$push": {"$concat": ["$data.tech_skills", "$data.soft_skills"]}}
                }},
                {"$sort": {"total_jobs": -1}},
                {"$limit": limit}
            ]
            
            company_data = await self.jobs_collection.aggregate(pipeline).to_list(None)
            
            company_insights = []
            for company_item in company_data:
                company_name = company_item["_id"]
                total_jobs = company_item["total_jobs"]
                
                # Flatten and count skills
                all_skills = []
                for skills_list in company_item["all_skills"]:
                    if isinstance(skills_list, list):
                        all_skills.extend(skills_list)
                
                # Get most common skills (top 5)
                skill_counts = {}
                for skill in all_skills:
                    if skill:
                        skill_counts[skill] = skill_counts.get(skill, 0) + 1
                
                common_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                common_skills = [skill for skill, count in common_skills]
                
                # Mock average salary (would be calculated from actual salary data)
                avg_salary = "$75-95k"
                
                company_insights.append(CompanyInsights(
                    company=company_name,
                    total_jobs=total_jobs,
                    avg_salary=avg_salary,
                    common_skills=common_skills,
                    job_types=list(set(company_item["job_types"])),
                    locations=list(set(company_item["locations"]))
                ))
            
            return company_insights
            
        except Exception as e:
            logger.error(f"Error calculating company insights: {e}")
            raise e
    
    async def generate_full_analytics(self) -> AnalyticsData:
        """Generate complete analytics data for the dashboard."""
        try:
            # Calculate all analytics components
            dashboard_stats = await self.calculate_dashboard_stats()
            top_skills = await self.calculate_top_skills()
            seniority_dist = await self.calculate_seniority_distribution()
            salary_ranges = await self.calculate_salary_ranges_by_level()
            company_insights = await self.calculate_company_insights()
            
            # Create analytics data object
            analytics_data = AnalyticsData(
                top_skills=top_skills,
                seniority_distribution=seniority_dist,
                salary_ranges_by_level=salary_ranges,
                company_insights=company_insights,
                dashboard_stats=dashboard_stats,
                calculated_at=datetime.utcnow()
            )
            
            # Store in analytics collection for caching
            await self.store_analytics(analytics_data)
            
            return analytics_data
            
        except Exception as e:
            logger.error(f"Error generating full analytics: {e}")
            raise e
    
    async def store_analytics(self, analytics: AnalyticsData) -> str:
        """Store analytics data in the database for caching."""
        try:
            # Remove old analytics data
            await self.analytics_collection.delete_many({})
            
            # Store new analytics data
            analytics_dict = analytics.dict(by_alias=True)
            result = await self.analytics_collection.insert_one(analytics_dict)
            
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Error storing analytics: {e}")
            raise e
    
    async def get_cached_analytics(self) -> Optional[AnalyticsData]:
        """Get cached analytics data if it exists and is recent."""
        try:
            # Get most recent analytics data
            analytics_doc = await self.analytics_collection.find_one(
                {},
                sort=[("calculated_at", -1)]
            )
            
            if analytics_doc:
                # Check if data is recent (less than 1 hour old)
                calculated_at = analytics_doc["calculated_at"]
                if datetime.utcnow() - calculated_at < timedelta(hours=1):
                    return AnalyticsData(**analytics_doc)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting cached analytics: {e}")
            return None
    
    async def get_skills_by_role(self) -> Dict[str, List[str]]:
        """Get skills mapped to different roles for filtering."""
        try:
            # This would be a more sophisticated calculation in a real system
            # For now, we'll return a basic mapping
            return {
                "Developer": ["JavaScript", "React", "Node.js", "Python", "Java", "C++", "Git", "SQL"],
                "Designer": ["Figma", "Adobe Creative Suite", "UI/UX", "Prototyping", "User Research"],
                "DevOps": ["Docker", "Kubernetes", "AWS", "Azure", "CI/CD", "Linux", "Shell Scripting"],
                "Data": ["Python", "SQL", "Machine Learning", "Data Analysis", "Statistics", "R"],
                "Product": ["Product Management", "User Research", "Analytics", "Strategy", "Agile"],
                "Marketing": ["Digital Marketing", "SEO", "Social Media", "Content Creation", "Analytics"],
                "Sales": ["CRM", "Lead Generation", "Negotiation", "Relationship Building", "Sales Strategy"]
            }
            
        except Exception as e:
            logger.error(f"Error getting skills by role: {e}")
            return {} 