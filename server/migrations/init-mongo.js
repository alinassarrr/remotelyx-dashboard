// MongoDB Initialization Script
// This script runs when the container starts for the first time

// Switch to the application database
db = db.getSiblingDB('remotelyx_dashboard');

// Create collections with indexes
db.createCollection('users');
db.createCollection('jobs');
db.createCollection('activities');
db.createCollection('analytics');

// Create indexes for better performance
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "created_at": 1 });

db.jobs.createIndex({ "user_id": 1 });
db.jobs.createIndex({ "status": 1 });
db.jobs.createIndex({ "created_at": 1 });
db.jobs.createIndex({ "company": 1 });

db.activities.createIndex({ "user_id": 1 });
db.activities.createIndex({ "job_id": 1 });
db.activities.createIndex({ "timestamp": 1 });

db.analytics.createIndex({ "user_id": 1 });
db.analytics.createIndex({ "date": 1 });
db.analytics.createIndex({ "metric_type": 1 });

print('Database initialized successfully!');
