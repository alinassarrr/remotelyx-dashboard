# 🗄️ Database Migrations & Seeding Guide

This guide explains how to use the migration and seeding system for RemotelyX.

## 🚀 Quick Start

### 1. Full Database Setup (Recommended for first time)

```bash
cd server
./db.sh setup
```

This will:

- Run all pending migrations
- Create collections with proper schemas
- Set up indexes for performance
- Populate with sample data

### 2. Check Current Status

```bash
./db.sh status
```

### 3. Run Only Migrations

```bash
./db.sh migrate
```

### 4. Run Only Seeds

```bash
./db.sh seed
```

## 🔧 Manual Usage

### Using Python directly:

```bash
cd server
poetry run python manage.py setup      # Full setup
poetry run python manage.py migrate    # Migrations only
poetry run python manage.py seed       # Seeds only
poetry run python manage.py status     # Check status
poetry run python manage.py reset      # Reset database
```

### Using Poetry shell:

```bash
cd server
poetry shell
python manage.py setup
```

## 📊 What Gets Created

### Migrations (Database Schema)

1. **001_create_users_collection** - Users collection with validation
2. **002_create_jobs_collection** - Jobs collection with validation
3. **003_create_activity_logs_collection** - Activity logging collection
4. **004_create_indexes** - Performance indexes
5. **005_add_user_roles_index** - Additional user role indexes

### Seeds (Sample Data)

1. **001_create_admin_user** - Default admin user

   - Email: `admin@remotelyx.com`
   - Password: `admin123`
   - Role: `admin`

2. **002_create_sample_jobs** - 5 sample job postings

   - Senior Backend Engineer (TechCorp)
   - Full Stack Developer (StartupXYZ)
   - Data Scientist (DataTech Inc)
   - DevOps Engineer (CloudSolutions)
   - Frontend Developer (WebDesign Pro)

3. **003_create_sample_activity_logs** - System activity logs

## 🏗️ Migration System Architecture

### Migration Manager

- Tracks applied migrations in `migrations` collection
- Ensures migrations run only once
- Maintains order of execution
- Provides rollback capability (planned)

### Schema Validation

- MongoDB schema validation for data integrity
- Proper field types and constraints
- Enum validation for status fields
- Required field enforcement

### Indexes

- Performance optimization for common queries
- Unique constraints (email, etc.)
- Compound indexes for complex queries

## 🌱 Seeding System

### Seed Manager

- Tracks applied seeds in `seeds` collection
- Prevents duplicate seeding
- Provides sample data for development
- Easy to extend with new seed data

### Sample Data Benefits

- **Development**: Ready-to-use data for testing
- **Demo**: Showcase features with realistic data
- **Testing**: Consistent test data across environments
- **Documentation**: Examples of data structure

## 🔄 Migration Workflow

### 1. Development

```bash
# Make changes to models/schemas
# Add new migration in migration_manager.py
# Test locally
./db.sh reset
./db.sh setup
```

### 2. Testing

```bash
# Verify migrations work correctly
./db.sh status
./db.sh migrate
./db.sh seed
```

### 3. Production

```bash
# Run migrations only (no seeds in production)
./db.sh migrate
```

## 📝 Adding New Migrations

### 1. Add Migration Function

```python
# In migration_manager.py
async def _add_new_feature(self):
    """Add new feature to database"""
    # Your migration logic here
    pass
```

### 2. Register Migration

```python
def get_available_migrations(self) -> List[str]:
    return [
        # ... existing migrations
        "006_add_new_feature"  # Add new migration
    ]

def get_migration_function(self, migration_name: str):
    migration_functions = {
        # ... existing functions
        "006_add_new_feature": self._add_new_feature  # Register function
    }
    return migration_functions.get(migration_name)
```

## 🌱 Adding New Seeds

### 1. Add Seed Function

```python
# In seed_manager.py
async def _create_new_sample_data(self):
    """Create new sample data"""
    # Your seeding logic here
    pass
```

### 2. Register Seed

```python
def get_available_seeds(self) -> List[str]:
    return [
        # ... existing seeds
        "004_create_new_sample_data"  # Add new seed
    ]

def get_seed_function(self, seed_name: str):
    seed_functions = {
        # ... existing functions
        "004_create_new_sample_data": self._create_new_sample_data  # Register function
    }
    return seed_functions.get(seed_name)
```

## 🚨 Important Notes

### Migration Safety

- Migrations are **idempotent** (safe to run multiple times)
- Each migration runs only once
- Migrations are tracked in database
- **Never modify existing migrations** - create new ones instead

### Seed Safety

- Seeds check for existing data before creating
- Safe to run multiple times
- Seeds are tracked in database
- **Seeds are for development/demo only** - not for production

### Database Reset

- `./db.sh reset` **drops all collections**
- **Use with caution** - this is destructive
- Only use in development
- Never use in production

## 🔍 Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**

   ```bash
   # Start MongoDB
   docker run -d -p 27017:27017 --name mongo mongo:latest
   ```

2. **Migration Already Applied**

   - Check status: `./db.sh status`
   - Reset if needed: `./db.sh reset`

3. **Import Errors**

   - Ensure you're in the server directory
   - Check Poetry environment: `poetry env info`

4. **Permission Denied**
   - Make scripts executable: `chmod +x *.sh`

### Debug Mode

```bash
# Run with verbose logging
poetry run python manage.py setup --verbose
```

## 📚 Best Practices

1. **Always backup** before running migrations in production
2. **Test migrations** in development first
3. **Use descriptive names** for migrations and seeds
4. **Keep migrations small** and focused
5. **Document complex migrations** with comments
6. **Version control** your migration files
7. **Run migrations** during maintenance windows

## 🎯 Next Steps

- [ ] Add rollback functionality
- [ ] Create migration templates
- [ ] Add data transformation migrations
- [ ] Implement migration testing framework
- [ ] Add production migration safety checks
