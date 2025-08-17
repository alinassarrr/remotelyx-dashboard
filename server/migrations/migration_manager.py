import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any
from bson import ObjectId
from app.core.database import get_collection

logger = logging.getLogger(__name__)

class MigrationManager:
	def __init__(self):
		self.migrations_collection = get_collection("migrations")
		
	async def ensure_migrations_collection(self):
		"""Ensure migrations collection exists and has proper indexes"""
		# Create unique index on migration name
		await self.migrations_collection.create_index("name", unique=True)
		# Create index on applied_at for ordering
		await self.migrations_collection.create_index("applied_at")
		
	async def get_applied_migrations(self) -> List[str]:
		"""Get list of already applied migration names"""
		cursor = self.migrations_collection.find({}, {"name": 1}).sort("applied_at", 1)
		migrations = await cursor.to_list(length=None)
		return [m["name"] for m in migrations]
		
	async def mark_migration_applied(self, name: str, details: Dict[str, Any] = None):
		"""Mark a migration as applied"""
		migration_record = {
			"name": name,
			"applied_at": datetime.utcnow(),
			"details": details or {}
		}
		await self.migrations_collection.insert_one(migration_record)
		logger.info(f"Migration '{name}' marked as applied")
		
	async def run_migration(self, name: str, migration_func):
		"""Run a specific migration"""
		try:
			logger.info(f"Running migration: {name}")
			await migration_func()
			await self.mark_migration_applied(name)
			logger.info(f"Migration '{name}' completed successfully")
			return True
		except Exception as e:
			logger.error(f"Migration '{name}' failed: {str(e)}")
			raise
			
	async def run_all_migrations(self):
		"""Run all pending migrations"""
		await self.ensure_migrations_collection()
		
		# Get all available migrations
		available_migrations = self.get_available_migrations()
		applied_migrations = await self.get_applied_migrations()
		
		# Find pending migrations
		pending_migrations = [
			name for name in available_migrations 
			if name not in applied_migrations
		]
		
		if not pending_migrations:
			logger.info("No pending migrations")
			return
			
		logger.info(f"Found {len(pending_migrations)} pending migrations")
		
		# Run migrations in order
		for migration_name in pending_migrations:
			migration_func = self.get_migration_function(migration_name)
			if migration_func:
				await self.run_migration(migration_name, migration_func)
			else:
				logger.warning(f"No migration function found for: {migration_name}")
				
	def get_available_migrations(self) -> List[str]:
		"""Get list of all available migration names in order"""
		return [
			"001_create_users_collection",
			"002_create_jobs_collection", 
			"003_create_activity_logs_collection",
			"004_create_indexes",
			"005_add_user_roles_index",
			"006_add_scraped_job_fields"
		]
		
	def get_migration_function(self, migration_name: str):
		"""Get the migration function by name"""
		migration_functions = {
			"001_create_users_collection": self._create_users_collection,
			"002_create_jobs_collection": self._create_jobs_collection,
			"003_create_activity_logs_collection": self._create_activity_logs_collection,
			"004_create_indexes": self._create_indexes,
			"005_add_user_roles_index": self._add_user_roles_index,
			"006_add_scraped_job_fields": self._add_scraped_job_fields
		}
		return migration_functions.get(migration_name)
		
	# Migration implementations
	async def _create_users_collection(self):
		"""Create users collection with proper schema validation"""
		db = get_collection("users").database
		
		# Check if collection exists
		collections = await db.list_collection_names()
		if "users" not in collections:
			await db.create_collection("users")
		
		# Add schema validation
		try:
			await db.command({
				"collMod": "users",
				"validator": {
					"$jsonSchema": {
						"bsonType": "object",
						"required": ["email", "password_hash", "role"],
						"properties": {
							"email": {
								"bsonType": "string",
								"pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
							},
							"password_hash": {"bsonType": "string"},
							"role": {
								"enum": ["admin", "user"]
							},
							"created_at": {"bsonType": "date"},
							"updated_at": {"bsonType": "date"}
						}
					}
				}
			})
		except Exception as e:
			logger.warning(f"Could not update users collection schema: {e}")
		
	async def _create_jobs_collection(self):
		"""Create jobs collection with proper schema validation"""
		db = get_collection("jobs").database
		
		# Check if collection exists
		collections = await db.list_collection_names()
		if "jobs" not in collections:
			await db.create_collection("jobs")
		
		# Add schema validation
		try:
			await db.command({
				"collMod": "jobs",
				"validator": {
					"$jsonSchema": {
						"bsonType": "object",
						"required": ["title", "company", "location", "type", "seniority", "salary_min", "salary_max"],
						"properties": {
							"title": {"bsonType": "string"},
							"company": {"bsonType": "string"},
							"location": {"bsonType": "string"},
							"type": {"enum": ["remote", "hybrid", "onsite"]},
							"seniority": {"enum": ["junior", "mid", "senior"]},
							"salary_min": {"bsonType": "int", "minimum": 0},
							"salary_max": {"bsonType": "int", "minimum": 0},
							"skills": {"bsonType": "array", "items": {"bsonType": "string"}},
							"status": {"enum": ["new", "analyzed", "matched", "closed"]}
						}
					}
				}
			})
		except Exception as e:
			logger.warning(f"Could not update jobs collection schema: {e}")
		
	async def _create_activity_logs_collection(self):
		"""Create activity_logs collection"""
		db = get_collection("activity_logs").database
		
		# Check if collection exists
		collections = await db.list_collection_names()
		if "activity_logs" not in collections:
			await db.create_collection("activity_logs")
		
	async def _create_indexes(self):
		"""Create database indexes for performance"""
		# Users collection indexes
		users_collection = get_collection("users")
		await users_collection.create_index("email", unique=True)
		await users_collection.create_index("role")
		
		# Jobs collection indexes
		jobs_collection = get_collection("jobs")
		await jobs_collection.create_index("title")
		await jobs_collection.create_index("company")
		await jobs_collection.create_index("location")
		await jobs_collection.create_index("type")
		await jobs_collection.create_index("seniority")
		await jobs_collection.create_index("status")
		await jobs_collection.create_index("posting_date")
		await jobs_collection.create_index("skills")
		
		# Activity logs indexes
		activity_collection = get_collection("activity_logs")
		await activity_collection.create_index("event")
		await activity_collection.create_index("timestamp")
		await activity_collection.create_index("job_id")
		await activity_collection.create_index("user_id")
		
	async def _add_user_roles_index(self):
		"""Add additional user roles index"""
		users_collection = get_collection("users")
		await users_collection.create_index([("role", 1), ("created_at", -1)])
		
	async def _add_scraped_job_fields(self):
		"""Add new fields and indexes required for scraped job data"""
		jobs_collection = get_collection("jobs")
		
		# Set defaults for new fields where missing
		await jobs_collection.update_many(
			{},
			{
				"$set": {
					"description": None,
					"employment_type": None,
					"job_link": None,
					"salary": None,
					"date_posted": None,
					"tech_skills": [],
					"soft_skills": [],
					"scraped_at": None,
					"posting_date": None
				}
			}
		)
		
		# Create indexes for scraped job features
		try:
			await jobs_collection.create_index("job_link")
			await jobs_collection.create_index("scraped_at")
			await jobs_collection.create_index("tech_skills")
			await jobs_collection.create_index("employment_type")
		except Exception as e:
			logger.warning(f"Index creation warning: {e}") 