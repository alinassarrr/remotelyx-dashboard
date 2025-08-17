from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.core.database import get_collection
from app.models.job_model import JobModel
from app.schemas.job_schema import JobCreate, JobUpdate, JobResponse, JobFilter
from bson import ObjectId

class JobService:
	def __init__(self, db=None):
		if db:
			self.collection = db["jobs"]
		else:
			self.collection = get_collection("jobs")

	async def create_job(self, job_data: JobCreate) -> JobResponse:
		"""Create a new job"""
		job_dict = job_data.dict()
		job_dict["posting_date"] = datetime.utcnow()
		job_dict["created_at"] = datetime.utcnow()
		job_dict["updated_at"] = datetime.utcnow()
		
		result = await self.collection.insert_one(job_dict)
		job_dict["_id"] = result.inserted_id
		
		return JobResponse(
			id=str(result.inserted_id),
			title=job_dict["title"],
			company=job_dict["company"],
			location=job_dict["location"],
			type=job_dict.get("type"),
			seniority=job_dict.get("seniority"),
			salary_min=job_dict.get("salary_min"),
			salary_max=job_dict.get("salary_max"),
			skills=job_dict.get("skills", []),
			posting_date=job_dict["posting_date"],
			status=job_dict.get("status", "new"),
			days_to_fill=job_dict.get("days_to_fill"),
			matched_date=job_dict.get("matched_date"),
			created_at=job_dict["created_at"],
			updated_at=job_dict["updated_at"]
		)

	async def get_jobs(self, filters: JobFilter, skip: int = 0, limit: int = 100, *, title_keyword: Optional[str] = None, employment_type: Optional[str] = None) -> List[JobResponse]:
		"""Get jobs with filters"""
		query: Dict[str, Any] = {}
		
		if filters.status:
			query["status"] = filters.status
		if filters.skills:
			query["skills"] = {"$in": filters.skills}
		if filters.seniority:
			query["seniority"] = filters.seniority
		if filters.company:
			query["company"] = {"$regex": filters.company, "$options": "i"}
		if filters.location:
			query["location"] = {"$regex": filters.location, "$options": "i"}
		if filters.type:
			query["type"] = filters.type
		if title_keyword:
			query["title"] = {"$regex": title_keyword, "$options": "i"}
		if employment_type:
			query["employment_type"] = employment_type
		if filters.salary_min is not None:
			query["salary_max"] = {"$gte": filters.salary_min}
		if filters.salary_max is not None:
			query["salary_min"] = {"$lte": filters.salary_max}
		if filters.date_from:
			query["posting_date"] = {"$gte": filters.date_from}
		if filters.date_to:
			if "posting_date" in query:
				query["posting_date"]["$lte"] = filters.date_to
			else:
				query["posting_date"] = {"$lte": filters.date_to}
		
		cursor = self.collection.find(query).skip(skip).limit(limit).sort("posting_date", -1)
		jobs: List[JobResponse] = []
		
		async for job in cursor:
			jobs.append(JobResponse(
				id=str(job["_id"]),
				title=job.get("title"),
				company=job.get("company"),
				location=job.get("location"),
				type=job.get("type"),
				seniority=job.get("seniority"),
				salary_min=job.get("salary_min"),
				salary_max=job.get("salary_max"),
				skills=job.get("skills", []),
				posting_date=job.get("posting_date"),
				status=job.get("status", "new"),
				days_to_fill=job.get("days_to_fill"),
				matched_date=job.get("matched_date"),
				created_at=job.get("created_at"),
				updated_at=job.get("updated_at")
			))
		
		return jobs

	async def get_job_by_id(self, job_id: str) -> Optional[JobResponse]:
		"""Get job by ID"""
		try:
			job = await self.collection.find_one({"_id": ObjectId(job_id)})
			if not job:
				return None
			
			return JobResponse(
				id=str(job["_id"]),
				title=job.get("title"),
				company=job.get("company"),
				location=job.get("location"),
				type=job.get("type"),
				seniority=job.get("seniority"),
				salary_min=job.get("salary_min"),
				salary_max=job.get("salary_max"),
				skills=job.get("skills", []),
				posting_date=job.get("posting_date"),
				status=job.get("status", "new"),
				days_to_fill=job.get("days_to_fill"),
				matched_date=job.get("matched_date"),
				created_at=job.get("created_at"),
				updated_at=job.get("updated_at")
			)
		except:
			return None

	async def update_job(self, job_id: str, job_data: JobUpdate) -> Optional[JobResponse]:
		"""Update job"""
		try:
			update_data = job_data.dict(exclude_unset=True)
			update_data["updated_at"] = datetime.utcnow()
			
			result = await self.collection.update_one(
				{"_id": ObjectId(job_id)},
				{"$set": update_data}
			)
			
			if result.modified_count == 0:
				return None
			
			return await self.get_job_by_id(job_id)
		except:
			return None

	async def delete_job(self, job_id: str) -> bool:
		"""Delete job"""
		try:
			result = await self.collection.delete_one({"_id": ObjectId(job_id)})
			return result.deleted_count > 0
		except:
			return False

	async def get_jobs_count(self, filters: JobFilter = None) -> int:
		"""Get total count of jobs with filters"""
		query: Dict[str, Any] = {}
		if filters:
			# Apply same filters as get_jobs
			if filters.status:
				query["status"] = filters.status
			if filters.skills:
				query["skills"] = {"$in": filters.skills}
			if filters.seniority:
				query["seniority"] = filters.seniority
			if filters.company:
				query["company"] = {"$regex": filters.company, "$options": "i"}
			if filters.location:
				query["location"] = {"$regex": filters.location, "$options": "i"}
			if filters.type:
				query["type"] = filters.type
			if filters.salary_min is not None:
				query["salary_max"] = {"$gte": filters.salary_min}
			if filters.salary_max is not None:
				query["salary_min"] = {"$lte": filters.salary_max}
			if filters.date_from:
				query["posting_date"] = {"$gte": filters.date_from}
			if filters.date_to:
				if "posting_date" in query:
					query["posting_date"]["$lte"] = filters.date_to
				else:
					query["posting_date"] = {"$lte": filters.date_to}
		
		return await self.collection.count_documents(query)

	async def get_distinct_filters(self) -> Dict[str, Any]:
		"""Return distinct values for filters needed in the frontend."""
		companies = await self.collection.distinct("company")
		seniorities = await self.collection.distinct("seniority")
		types = await self.collection.distinct("type")
		statuses = await self.collection.distinct("status")
		employment_types = await self.collection.distinct("employment_type")
		tech_skills = await self.collection.distinct("tech_skills")
		
		return {
			"companies": sorted([c for c in companies if c]),
			"seniority": sorted([s for s in seniorities if s]),
			"types": sorted([t for t in types if t]),
			"statuses": sorted([s for s in statuses if s]),
			"employment_types": sorted([e for e in employment_types if e]),
			"tech_skills": sorted([s for s in tech_skills if s])
		}

	async def find_duplicate_job(self, company: str, title: str, job_link: str = None) -> Optional[JobModel]:
		"""Find duplicate job by company, title and optionally job_link"""
		query = {
			"company": {"$regex": f"^{company}$", "$options": "i"},
			"title": {"$regex": f"^{title}$", "$options": "i"}
		}
		
		if job_link:
			query["job_link"] = job_link
		
		job = await self.collection.find_one(query)
		if job:
			return JobModel(**job)
		return None

	async def create_job_from_model(self, job_model: JobModel) -> JobModel:
		"""Create a new job from JobModel"""
		job_dict = job_model.dict(exclude={"id"})
		result = await self.collection.insert_one(job_dict)
		job_dict["_id"] = result.inserted_id
		return JobModel(**job_dict)

	async def update_job_from_dict(self, job_id: str, update_data: dict) -> Optional[JobModel]:
		"""Update job with dict data (used by scraper)."""
		try:
			update_data["updated_at"] = datetime.utcnow()
			result = await self.collection.update_one(
				{"_id": ObjectId(job_id)},
				{"$set": update_data}
			)
			
			if result.modified_count == 0:
				return None
			
			updated_job = await self.collection.find_one({"_id": ObjectId(job_id)})
			if updated_job:
				return JobModel(**updated_job)
			return None
		except:
			return None

	async def count_jobs(self) -> int:
		"""Get total count of all jobs"""
		return await self.collection.count_documents({})

	async def count_jobs_with_scraped_data(self) -> int:
		"""Count jobs that have scraped_at timestamp (i.e., came from scraper)"""
		return await self.collection.count_documents({"scraped_at": {"$exists": True}})

	async def get_recently_scraped_jobs(self, days: int = 7) -> List[JobModel]:
		"""Get jobs scraped within the last N days"""
		cutoff_date = datetime.utcnow() - timedelta(days=days)
		cursor = self.collection.find({
			"scraped_at": {"$gte": cutoff_date}
		}).sort("scraped_at", -1)
		
		jobs: List[JobModel] = []
		async for job in cursor:
			jobs.append(JobModel(**job))
		return jobs 