#!/usr/bin/env python3
"""
Database Status Checker for RemotelyX Backend
"""
import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

from app.core.database import connect_to_mongo, close_mongo_connection
from app.services.seeder_service import SeederService

async def check_database_status():
    """Check the current status of the database."""
    try:
        print("🔍 Checking database status...")
        
        # Connect to MongoDB
        await connect_to_mongo()
        print("✅ Connected to MongoDB")
        
        # Get seeder service
        seeder = SeederService()
        
        # Check current status
        status = await seeder.get_seeding_status()
        
        print("\n📊 Database Status:")
        print(f"   Total Jobs: {status['total_jobs']}")
        print(f"   Has Data: {status['has_data']}")
        print(f"   Sample Jobs: {status['sample_jobs_count']}")
        print(f"   Last Updated: {status['last_updated']}")
        
        if status['has_data']:
            print("\n⚠️  Database already contains data!")
            print("   Use the seeder endpoints to clear data if needed:")
            print("   DELETE /api/v1/seeder/clear")
        else:
            print("\n✅ Database is empty and ready for fresh data!")
        
        await close_mongo_connection()
        print("\n✅ Database connection closed")
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(check_database_status()) 