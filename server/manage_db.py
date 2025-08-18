#!/usr/bin/env python3
"""
Database Management Script for RemotelyX Backend
"""
import asyncio
import sys
import os

sys.path.append(os.path.dirname(__file__))

from app.core.database import connect_to_mongo, close_mongo_connection
from app.services.seeder_service import SeederService

async def check_status():
    """Check database status."""
    try:
        await connect_to_mongo()
        seeder = SeederService()
        status = await seeder.get_seeding_status()
        
        print("\n📊 Database Status:")
        print(f"   Total Jobs: {status['total_jobs']}")
        print(f"   Has Data: {status['has_data']}")
        print(f"   Sample Jobs: {status['sample_jobs_count']}")
        print(f"   Last Updated: {status['last_updated']}")
        
        await close_mongo_connection()
        
    except Exception as e:
        print(f"❌ Error: {e}")

async def clear_database():
    """Clear all data from database."""
    try:
        await connect_to_mongo()
        seeder = SeederService()
        
        print("🗑️  Clearing database...")
        await seeder.clear_all_jobs()
        print("✅ Database cleared")
        
        await close_mongo_connection()
        
    except Exception as e:
        print(f"❌ Error: {e}")

async def seed_sample_data():
    """Seed database with sample data."""
    try:
        await connect_to_mongo()
        seeder = SeederService()
        
        print("📊 Seeding sample data...")
        job_ids = await seeder.seed_sample_jobs(50)
        print(f"✅ Created {len(job_ids)} sample jobs")
        
        await close_mongo_connection()
        
    except Exception as e:
        print(f"❌ Error: {e}")

async def seed_example_n8n():
    """Seed database with example n8n data."""
    try:
        await connect_to_mongo()
        seeder = SeederService()
        
        print("📊 Seeding example n8n data...")
        job_ids = await seeder.seed_example_n8n_data()
        print(f"✅ Created {len(job_ids)} example jobs")
        
        await close_mongo_connection()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def show_menu():
    """Show the main menu."""
    print("\n🔧 RemotelyX Database Management")
    print("=" * 40)
    print("1. Check Database Status")
    print("2. Clear All Data")
    print("3. Seed Sample Data (50 jobs)")
    print("4. Seed Example n8n Data")
    print("5. Run Full Database Setup")
    print("6. Exit")
    print("=" * 40)

async def main():
    """Main function."""
    while True:
        show_menu()
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == "1":
            await check_status()
        elif choice == "2":
            confirm = input("⚠️  Are you sure you want to clear all data? (yes/no): ").strip().lower()
            if confirm == "yes":
                await clear_database()
            else:
                print("❌ Operation cancelled")
        elif choice == "3":
            await seed_sample_data()
        elif choice == "4":
            await seed_example_n8n()
        elif choice == "5":
            print("🚀 Running full database setup...")
            os.system("python3 setup_database.py")
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}") 