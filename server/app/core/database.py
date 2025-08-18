from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING, TEXT
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def connect_to_mongo():
    """Create database connection."""
    try:
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db.db = db.client[settings.MONGODB_DB]
        
        # Create collections
        await create_collections()
        
        # Create indexes for better performance
        await create_indexes()
        
        logger.info("Connected to MongoDB.")
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """Close database connection."""
    try:
        if db.client:
            db.client.close()
            logger.info("Closed MongoDB connection.")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {e}")

async def create_collections():
    """Create necessary collections if they don't exist."""
    try:
        # Get list of existing collections
        existing_collections = await db.db.list_collection_names()
        
        # Create jobs collection
        if "jobs" not in existing_collections:
            await db.db.create_collection("jobs")
            logger.info("Created 'jobs' collection")
        
        # Create analytics collection
        if "analytics" not in existing_collections:
            await db.db.create_collection("analytics")
            logger.info("Created 'analytics' collection")
            
        # Create skills collection for caching
        if "skills_cache" not in existing_collections:
            await db.db.create_collection("skills_cache")
            logger.info("Created 'skills_cache' collection")
            
    except Exception as e:
        logger.error(f"Error creating collections: {e}")

async def create_indexes():
    """Create database indexes for optimal query performance."""
    try:
        # Jobs collection indexes
        jobs_collection = db.db.jobs
        
        # Text search index for job search
        await jobs_collection.create_index([
            ("data.title", TEXT),
            ("data.company", TEXT),
            ("data.description", TEXT),
            ("data.tech_skills", TEXT),
            ("data.soft_skills", TEXT)
        ])
        
        # Single field indexes for filtering
        await jobs_collection.create_index("data.company", ASCENDING)
        await jobs_collection.create_index("data.location", ASCENDING)
        await jobs_collection.create_index("data.seniority", ASCENDING)
        await jobs_collection.create_index("data.employment_type", ASCENDING)
        await jobs_collection.create_index("data.scraped_at", DESCENDING)
        await jobs_collection.create_index("created_at", DESCENDING)
        
        # Compound index for date range queries
        await jobs_collection.create_index([
            ("created_at", DESCENDING),
            ("data.company", ASCENDING)
        ])
        
        # Analytics collection indexes
        analytics_collection = db.db.analytics
        await analytics_collection.create_index("calculated_at", DESCENDING)
        
        # Skills cache collection indexes
        skills_collection = db.db.skills_cache
        await skills_collection.create_index("skill", ASCENDING)
        await skills_collection.create_index("updated_at", DESCENDING)
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.error(f"Error creating indexes: {e}")

def get_collection(collection_name: str):
    """Get a collection by name."""
    return db.db[collection_name]

# Collection names
JOBS_COLLECTION = "jobs"
ANALYTICS_COLLECTION = "analytics"
SKILLS_CACHE_COLLECTION = "skills_cache" 