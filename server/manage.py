#!/usr/bin/env python3
"""
RemotelyX Database Management Script

Usage:
    python manage.py migrate          # Run all pending migrations
    python manage.py seed             # Run all pending seeds
    python manage.py reset            # Reset database (drop all collections)
    python manage.py status           # Show migration and seed status
    python manage.py setup            # Run migrations + seeds (full setup)
"""

import asyncio
import sys
import logging
from typing import Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def run_migrations():
    """Run all pending migrations"""
    try:
        from migrations.migration_manager import MigrationManager
        
        print("🔄 Running migrations...")
        migration_manager = MigrationManager()
        await migration_manager.run_all_migrations()
        print("✅ Migrations completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        sys.exit(1)

async def run_seeds():
    """Run all pending seeds"""
    try:
        from seeds.seed_manager import SeedManager
        
        print("🌱 Running seeds...")
        seed_manager = SeedManager()
        await seed_manager.run_all_seeds()
        print("✅ Seeds completed successfully!")
        
    except Exception as e:
        print(f"❌ Seeding failed: {str(e)}")
        sys.exit(1)

async def reset_database():
    """Reset database by dropping all collections"""
    try:
        from app.core.database import get_collection
        
        print("⚠️  Resetting database...")
        
        # Get all collections
        db = get_collection("users").database
        collections = await db.list_collection_names()
        
        # Drop all collections except system ones
        for collection_name in collections:
            if not collection_name.startswith("system."):
                await db.drop_collection(collection_name)
                print(f"   Dropped collection: {collection_name}")
                
        print("✅ Database reset completed!")
        
    except Exception as e:
        print(f"❌ Database reset failed: {str(e)}")
        sys.exit(1)

async def show_status():
    """Show migration and seed status"""
    try:
        from migrations.migration_manager import MigrationManager
        from seeds.seed_manager import SeedManager
        
        print("📊 Database Status")
        print("=" * 50)
        
        # Migration status
        print("\n🔄 Migrations:")
        migration_manager = MigrationManager()
        await migration_manager.ensure_migrations_collection()
        
        available_migrations = migration_manager.get_available_migrations()
        applied_migrations = await migration_manager.get_applied_migrations()
        
        for migration in available_migrations:
            status = "✅ Applied" if migration in applied_migrations else "⏳ Pending"
            print(f"   {migration}: {status}")
            
        # Seed status
        print("\n🌱 Seeds:")
        seed_manager = SeedManager()
        await seed_manager.ensure_seeds_collection()
        
        available_seeds = seed_manager.get_available_seeds()
        applied_seeds = await seed_manager.get_applied_seeds()
        
        for seed in available_seeds:
            status = "✅ Applied" if seed in applied_seeds else "⏳ Pending"
            print(f"   {seed}: {status}")
            
        print("\n" + "=" * 50)
        
    except Exception as e:
        print(f"❌ Status check failed: {str(e)}")
        sys.exit(1)

async def setup_database():
    """Run full database setup (migrations + seeds)"""
    print("🚀 Setting up database...")
    print("=" * 50)
    
    await run_migrations()
    print()
    await run_seeds()
    print()
    print("🎉 Database setup completed successfully!")

def print_usage():
    """Print usage information"""
    print(__doc__)

async def main():
    """Main function"""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
        
    command = sys.argv[1].lower()
    
    # Initialize database connection
    try:
        from app.core.database import connect_to_mongo
        await connect_to_mongo()
    except Exception as e:
        print(f"❌ Failed to connect to database: {str(e)}")
        sys.exit(1)
    
    try:
        if command == "migrate":
            await run_migrations()
        elif command == "seed":
            await run_seeds()
        elif command == "reset":
            await reset_database()
        elif command == "status":
            await show_status()
        elif command == "setup":
            await setup_database()
        else:
            print(f"❌ Unknown command: {command}")
            print_usage()
            sys.exit(1)
            
    finally:
        # Close database connection
        try:
            from app.core.database import close_mongo_connection
            await close_mongo_connection()
        except:
            pass

if __name__ == "__main__":
    asyncio.run(main()) 