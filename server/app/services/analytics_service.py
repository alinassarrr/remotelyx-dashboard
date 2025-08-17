from typing import List, Dict, Any, Optional
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

	async def _week_range(self):
		"""Return datetime bounds for current and previous weeks"""
		now = datetime.utcnow()
		current_week_start = now - timedelta(days=now.weekday())
		previous_week_start = current_week_start - timedelta(days=7)
		return current_week_start, previous_week_start

	async def get_kpis(self) -> KPIs:
		"""Calculate key performance indicators with weekly deltas"""
		# Totals
		total_jobs = await self.jobs_collection.count_documents({})
		active_jobs = await self.jobs_collection.count_documents({"status": {"$ne": "closed"}})
		
		# New jobs this week with delta vs previous week
		current_week_start, previous_week_start = await self._week_range()
		week_ago = current_week_start
		prev_week_ago = previous_week_start
		
		new_this_week = await self.jobs_collection.count_documents({
			"posting_date": {"$gte": week_ago}
		})
		new_prev_week = await self.jobs_collection.count_documents({
			"posting_date": {"$gte": prev_week_ago, "$lt": week_ago}
		})
		delta_new_this_week = 0.0
		if new_prev_week > 0:
			delta_new_this_week = ((new_this_week - new_prev_week) / new_prev_week) * 100
		
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
			total_jobs=total_jobs,
			new_this_week_delta=round(delta_new_this_week, 2)
		)

	async def get_skills_demand(self, title_keyword: Optional[str] = None, market: Optional[str] = None) -> List[SkillDemand]:
		"""Get skills demand analysis, optionally filtered by job title keyword and market."""
		match_stage: Dict[str, Any] = {}
		if title_keyword:
			match_stage["title"] = {"$regex": title_keyword, "$options": "i"}
		# Example market filter placeholder; real implementation would require a location-to-market mapping
		if market and market.upper() == "US":
			# Simple heuristic: include jobs with 'Remote' or locations containing US states/US keywords in production
			pass
		
		pipeline = []
		if match_stage:
			pipeline.append({"$match": match_stage})
		pipeline.extend([
			{"$unwind": "$tech_skills"},
			{"$group": {"_id": "$tech_skills", "count": {"$sum": 1}}},
			{"$sort": {"count": -1}},
			{"$limit": 25}
		])
		
		skills_data = await self.jobs_collection.aggregate(pipeline).to_list(length=None)
		
		# Total jobs under same filter (for percentages)
		total_jobs = await self.jobs_collection.count_documents(match_stage if match_stage else {})
		
		skills_demand: List[SkillDemand] = []
		for skill in skills_data:
			percentage = (skill["count"] / total_jobs) * 100 if total_jobs > 0 else 0
			skills_demand.append(SkillDemand(
				skill=skill["_id"],
				count=skill["count"],
				percentage=round(percentage, 2)
			))
		
		return skills_demand

	async def get_seniority_distribution(self, title_keyword: Optional[str] = None) -> List[SeniorityDistribution]:
		"""Get seniority distribution, optionally filtered by job title keyword."""
		match_stage: Dict[str, Any] = {}
		if title_keyword:
			match_stage["title"] = {"$regex": title_keyword, "$options": "i"}
		pipeline = []
		if match_stage:
			pipeline.append({"$match": match_stage})
		pipeline.extend([
			{"$group": {"_id": "$seniority", "count": {"$sum": 1}}},
			{"$sort": {"count": -1}}
		])
		
		data = await self.jobs_collection.aggregate(pipeline).to_list(length=None)
		total = await self.jobs_collection.count_documents(match_stage if match_stage else {})
		
		result: List[SeniorityDistribution] = []
		for item in data:
			percentage = (item["count"] / total) * 100 if total > 0 else 0
			result.append(SeniorityDistribution(
				seniority=item["_id"],
				count=item["count"],
				percentage=round(percentage, 2)
			))
		return result

	async def get_trending_skills(self, title_keyword: Optional[str] = None) -> List[TrendingSkill]:
		"""Trending skills week-over-week, optionally filtered by job title keyword."""
		now = datetime.utcnow()
		current_week_start = now - timedelta(days=now.weekday())
		previous_week_start = current_week_start - timedelta(days=7)
		
		match_current: Dict[str, Any] = {"posting_date": {"$gte": current_week_start}}
		match_previous: Dict[str, Any] = {"posting_date": {"$gte": previous_week_start, "$lt": current_week_start}}
		if title_keyword:
			match_current["title"] = {"$regex": title_keyword, "$options": "i"}
			match_previous["title"] = {"$regex": title_keyword, "$options": "i"}
		
		current_week_pipeline = [
			{"$match": match_current},
			{"$unwind": "$tech_skills"},
			{"$group": {"_id": "$tech_skills", "count": {"$sum": 1}}},
			{"$sort": {"count": -1}},
			{"$limit": 15}
		]
		previous_week_pipeline = [
			{"$match": match_previous},
			{"$unwind": "$tech_skills"},
			{"$group": {"_id": "$tech_skills", "count": {"$sum": 1}}},
			{"$sort": {"count": -1}},
			{"$limit": 15}
		]
		
		current_week_skills = await self.jobs_collection.aggregate(current_week_pipeline).to_list(length=None)
		previous_week_skills = await self.jobs_collection.aggregate(previous_week_pipeline).to_list(length=None)
		
		current_week_dict = {s["_id"]: s["count"] for s in current_week_skills}
		previous_week_dict = {s["_id"]: s["count"] for s in previous_week_skills}
		
		trending: List[TrendingSkill] = []
		for skill_name, cur_count in current_week_dict.items():
			prev_count = previous_week_dict.get(skill_name, 0)
			growth_percentage = 0
			if prev_count > 0:
				growth_percentage = ((cur_count - prev_count) / prev_count) * 100
			trending.append(TrendingSkill(
				skill=skill_name,
				current_week_count=cur_count,
				previous_week_count=prev_count,
				growth_percentage=round(growth_percentage, 2)
			))
		
		trending.sort(key=lambda x: x.growth_percentage, reverse=True)
		return trending[:10]

	async def get_hard_to_fill_roles(self) -> List[HardToFillRole]:
		"""Get roles that are hard to fill (high average days to fill)"""
		pipeline = [
			{"$match": {"days_to_fill": {"$exists": True, "$ne": None}}},
			{"$group": {"_id": "$title", "avg_days_to_fill": {"$avg": "$days_to_fill"}, "job_count": {"$sum": 1}}},
			{"$match": {"job_count": {"$gte": 3}}},  # Only roles with at least 3 jobs
			{"$sort": {"avg_days_to_fill": -1}},
			{"$limit": 10}
		]
		
		rows = await self.jobs_collection.aggregate(pipeline).to_list(length=None)
		return [
			HardToFillRole(title=r["_id"], avg_days_to_fill=round(r["avg_days_to_fill"], 1), job_count=r["job_count"]) 
			for r in rows
		]

	async def get_recent_activity(self, limit: int = 20) -> List[RecentActivity]:
		"""Get recent activity logs"""
		cursor = self.activity_collection.find().sort("timestamp", -1).limit(limit)
		result: List[RecentActivity] = []
		async for activity in cursor:
			result.append(RecentActivity(
				event=activity["event"],
				timestamp=activity["timestamp"],
				details=activity.get("details", {})
			))
		return result

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