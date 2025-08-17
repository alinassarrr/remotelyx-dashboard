# 🔄 n8n MongoDB Integration Guide

## 📋 Overview

This guide shows how to configure n8n workflows to insert data directly into MongoDB, sharing the same database as your RemotelyX backend.

## 🗄️ MongoDB Connection Details for n8n

### Connection Information

- **Host**: `mongodb` (internal Docker network)
- **Port**: `27017`
- **Username**: `admin`
- **Password**: `password123`
- **Database**: `remotelyx_dashboard`
- **Authentication Database**: `admin`

### Full Connection String

```
mongodb://admin:password123@mongodb:27017/remotelyx_dashboard?authSource=admin
```

## 🔧 Setting up MongoDB Node in n8n

### 1. Access n8n

#### Local Access

- Open http://localhost:5679
- Login with: `hadihaidar1723@gmail.com` / `Treble23!`

#### Public Access (with ngrok)

If you need public webhooks or OAuth integrations:

1. **Install ngrok**: https://ngrok.com/
2. **Expose n8n**: `ngrok http 5679`
3. **Configure**: Run `setup-ngrok.bat` (Windows) or `setup-ngrok.sh` (Linux/Mac)
4. **Access**: Use your ngrok URL (e.g., https://abc123.ngrok.io)

### 2. Create MongoDB Connection

1. **Add MongoDB Node**

   - Drag "MongoDB" node to your workflow
   - Click on the MongoDB node to configure

2. **Configure Connection**

   ```
   Host: mongodb
   Port: 27017
   Database: remotelyx_dashboard
   Username: admin
   Password: password123
   Authentication Database: admin
   ```

3. **Test Connection**
   - Click "Test Connection" to verify

## 📊 Available Collections

The RemotelyX database includes these collections:

| Collection   | Purpose                       | Key Fields                                                             |
| ------------ | ----------------------------- | ---------------------------------------------------------------------- |
| `jobs`       | Job postings and applications | `title`, `company`, `location`, `salary`, `tech_skills`, `soft_skills` |
| `users`      | User accounts                 | `email`, `name`, `role`, `created_at`                                  |
| `activities` | User activity tracking        | `user_id`, `job_id`, `activity_type`, `timestamp`                      |
| `analytics`  | Analytics data                | `user_id`, `metric_type`, `value`, `date`                              |

## 🚀 Example n8n Workflows

### 1. Job Scraper to MongoDB Workflow

```
HTTP Request → Function → MongoDB Insert
```

**Step-by-step:**

1. **HTTP Request Node**

   - URL: `http://backend:8000/api/v1/scraper/scrape`
   - Method: `POST`
   - Body: `{"job_url": "{{ $json.job_url }}"}`

2. **Function Node (Optional - Data Transformation)**

   ```javascript
   // Transform scraped data if needed
   const scrapedData = items[0].json.data;

   return [
     {
       json: {
         ...scrapedData,
         scraped_at: new Date().toISOString(),
         source: "n8n_workflow",
         processed: true,
       },
     },
   ];
   ```

3. **MongoDB Insert Node**
   - Operation: `Insert`
   - Collection: `jobs`
   - Data: `{{ $json }}`

### 2. Bulk Job Import Workflow

```
Schedule Trigger → Read URLs → Loop → HTTP Request → MongoDB Insert
```

**Configuration:**

1. **Schedule Trigger**

   - Interval: Every hour
   - Or manual trigger

2. **Function Node (URL List)**

   ```javascript
   const jobUrls = [
     "https://example.com/job1",
     "https://example.com/job2",
     "https://example.com/job3",
   ];

   return jobUrls.map((url) => ({ json: { job_url: url } }));
   ```

3. **HTTP Request Node**

   - URL: `http://backend:8000/api/v1/scraper/scrape`
   - Method: `POST`
   - Body: `{"job_url": "{{ $json.job_url }}"}`

4. **MongoDB Insert Node**
   - Collection: `jobs`
   - Data: `{{ $json.data }}`

### 3. Data Validation and Enrichment

```
MongoDB Find → Function (Validate) → MongoDB Update
```

**Use Case**: Clean and enrich existing job data

1. **MongoDB Find Node**

   - Collection: `jobs`
   - Query: `{"processed": {"$ne": true}}`

2. **Function Node (Data Enrichment)**

   ```javascript
   const jobData = items[0].json;

   // Add computed fields
   const enrichedData = {
     ...jobData,
     skill_count:
       (jobData.tech_skills || []).length + (jobData.soft_skills || []).length,
     has_salary: !!jobData.salary && jobData.salary !== "Not specified",
     experience_level: jobData.seniority || "Not specified",
     processed: true,
     enriched_at: new Date().toISOString(),
   };

   return [{ json: enrichedData }];
   ```

3. **MongoDB Update Node**
   - Collection: `jobs`
   - Query: `{"_id": "{{ $json._id }}"}`
   - Update: `{{ $json }}`

## 🔍 MongoDB Query Examples

### Find Jobs by Skills

```javascript
// In MongoDB node query field
{
  "tech_skills": { "$in": ["Python", "JavaScript", "React"] }
}
```

### Find Recent Jobs

```javascript
{
  "created_at": {
    "$gte": new Date(Date.now() - 7*24*60*60*1000) // Last 7 days
  }
}
```

### Aggregate by Company

```javascript
// Use MongoDB Aggregate node
[
  {
    $group: {
      _id: "$company",
      job_count: { $sum: 1 },
      avg_skills: { $avg: { $size: "$tech_skills" } },
    },
  },
  {
    $sort: { job_count: -1 },
  },
];
```

## 📈 Analytics Workflows

### 1. Daily Job Stats

```
Schedule → MongoDB Aggregate → MongoDB Insert (analytics)
```

**Aggregation Pipeline:**

```javascript
[
  {
    $match: {
      created_at: {
        $gte: new Date(Date.now() - 24 * 60 * 60 * 1000),
      },
    },
  },
  {
    $group: {
      _id: null,
      total_jobs: { $sum: 1 },
      unique_companies: { $addToSet: "$company" },
      avg_salary: { $avg: "$salary_numeric" },
    },
  },
  {
    $project: {
      _id: 0,
      date: new Date().toISOString().split("T")[0],
      total_jobs: 1,
      unique_companies: { $size: "$unique_companies" },
      avg_salary: 1,
      metric_type: "daily_stats",
    },
  },
];
```

### 2. Skill Demand Analysis

```javascript
// Unwind tech_skills and count frequency
[
  { $unwind: "$tech_skills" },
  {
    $group: {
      _id: "$tech_skills",
      demand_count: { $sum: 1 },
    },
  },
  { $sort: { demand_count: -1 } },
  { $limit: 20 },
];
```

## 🔄 Webhook Integration

### Receive Job URLs via Webhook

1. **Webhook Trigger**

   - HTTP Method: `POST`
   - Response Mode: `On Received`

2. **Function Node (Validate Input)**

   ```javascript
   const { job_url } = items[0].json;

   if (!job_url || !job_url.startsWith("http")) {
     throw new Error("Invalid job URL provided");
   }

   return [{ json: { job_url } }];
   ```

3. **HTTP Request to Scraper**
4. **MongoDB Insert**

**Webhook URLs**:

- Local: `http://localhost:5679/webhook/job-scraper`
- Public (ngrok): `https://your-ngrok-url.ngrok.io/webhook/job-scraper`

## 🛡️ Error Handling

### Add Error Handling to Workflows

1. **Try-Catch Pattern**

   ```javascript
   // In Function node
   try {
     // Your processing logic
     const result = processJobData(items[0].json);
     return [{ json: result }];
   } catch (error) {
     // Log error to MongoDB
     return [
       {
         json: {
           error: error.message,
           timestamp: new Date().toISOString(),
           input_data: items[0].json,
         },
       },
     ];
   }
   ```

2. **MongoDB Error Collection**
   - Create separate collection for errors
   - Log failed operations for debugging

## 📊 Monitoring and Maintenance

### 1. Workflow Health Check

```javascript
// Check if workflows are running properly
{
  "workflow_name": "job_scraper",
  "last_run": { "$gte": new Date(Date.now() - 60*60*1000) }, // Last hour
  "status": "success"
}
```

### 2. Data Quality Checks

```javascript
// Find jobs missing required fields
{
  "$or": [
    { "title": { "$exists": false } },
    { "company": { "$exists": false } },
    { "tech_skills": { "$size": 0 } }
  ]
}
```

## 🔧 Performance Tips

1. **Use Indexes**: Ensure MongoDB collections have proper indexes
2. **Batch Operations**: Use bulk insert for multiple records
3. **Limit Results**: Always use `.limit()` for large datasets
4. **Connection Pooling**: Reuse MongoDB connections in workflows

## 🚀 Advanced Integration

### Connect to External APIs

```javascript
// Enrich job data with external APIs
const jobTitle = items[0].json.title;
const companyName = items[0].json.company;

// Call external API for company information
const companyInfo = await fetch(
  `https://api.company-data.com/search?name=${companyName}`
);

return [
  {
    json: {
      ...items[0].json,
      company_info: companyInfo,
      enriched: true,
    },
  },
];
```

---

**🎉 You now have a complete n8n + MongoDB integration for automated job data processing!**
