"""Database utility functions."""

import motor.motor_asyncio
from app.core.config import settings

# Database connection
client = None
database = None


async def get_database():
    """Get database instance for dependency injection."""
    global client, database
    
    if database is None:
        client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
        database = client[settings.MONGODB_DB]
    
    return database


async def close_database_connection():
    """Close database connection."""
    global client
    if client:
        client.close()
