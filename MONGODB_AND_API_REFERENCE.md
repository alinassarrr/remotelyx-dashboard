# 📊 MongoDB Collections & Backend APIs Reference

This document shows the current MongoDB collections structure and backend APIs for your RemotelyX Dashboard frontend.

## 🗄️ **MongoDB Collections Structure**

### **📋 Jobs Collection** (`jobs`)

**Collection Name:** `jobs`  
**Total Documents:** 3 (sample data)  
**Scraped Jobs:** 3  
**Manual Jobs:** 0

#### **Document Schema:**

```json
{
  "_id": "68a133c8b639eadc6cfd5b73",
  "title": "Full Stack Developer - IC",
  "company": "Gamma",
  "location": "Remote",
  "description": "We are looking for a highly skilled Full-Stack Developer with 3+ years of experience...",

  // New scraped job fields
  "employment_type": "Full-time",
  "job_link": "https://gamma.app/docs/full-stack-developer-ic-3s64m1oqf3nuf5u?mode=doc",
  "salary": "$2,500+",
  "date_posted": "Not specified",
  "scraped_at": "2025-08-17T01:43:36.748Z",

  // Skills categorization
  "tech_skills": [
    "React.js",
    "Next.js",
    "Node.js",
    "Nest.js",
    "MySQL",
    "PostgreSQL"
  ],
  "soft_skills": ["communication", "leadership", "teamwork", "problem-solving"],
  "skills": ["React.js", "Next.js", "Node.js", "communication", "leadership"], // Combined for backward compatibility

  // Job details
  "seniority": "mid", // "junior", "mid", "senior"
  "type": "remote", // "remote", "hybrid", "onsite"
  "salary_min": 2500,
  "salary_max": 5000,
  "status": "new", // "new", "analyzed", "matched", "closed"

  // Timestamps
  "created_at": "2025-08-17T01:43:36.748Z",
  "updated_at": "2025-08-17T01:43:36.748Z"
}
```

#### **Current Sample Companies:**

- Gamma
- TechStartup Inc
- CloudTech Solutions

#### **Skills Distribution:**

- **Jobs with tech_skills:** 3/3 (100%)
- **Jobs with soft_skills:** 3/3 (100%)
- **Average tech skills per job:** 6
- **Average soft skills per job:** 4

---

## 🔌 **Backend API Endpoints**

### **🏥 Health Check**

```http
GET /health
```

**Response:**

```json
{
  "status": "healthy",
  "service": "RemotelyX API"
}
```

---

### **💼 Job Management APIs**

#### **1. Get All Jobs**

```http
GET /api/v1/jobs?skip=0&limit=20
```

**Query Parameters:**

- `skip` (int): Number of jobs to skip (pagination)
- `limit` (int): Maximum jobs to return (default: 20)

**Response:**

```json
[
  {
    "id": "68a133c8b639eadc6cfd5b73",
    "title": "Full Stack Developer - IC",
    "company": "Gamma",
    "location": "Remote",
    "description": "We are looking for a highly skilled Full-Stack Developer...",
    "employment_type": "Full-time",
    "job_link": "https://gamma.app/docs/full-stack-developer...",
    "salary": "$2,500+",
    "date_posted": "Not specified",
    "tech_skills": ["React.js", "Next.js", "Node.js", "Nest.js"],
    "soft_skills": ["communication", "leadership", "teamwork"],
    "skills": ["React.js", "Next.js", "Node.js", "communication"],
    "seniority": "mid",
    "type": "remote",
    "salary_min": 2500,
    "salary_max": 5000,
    "scraped_at": "2025-08-17T01:43:36.748Z",
    "status": "new",
    "created_at": "2025-08-17T01:43:36.748Z",
    "updated_at": "2025-08-17T01:43:36.748Z"
  }
]
```

#### **2. Get Single Job**

```http
GET /api/v1/jobs/{job_id}
```

#### **3. Create Job**

```http
POST /api/v1/jobs
Content-Type: application/json

{
  "title": "Senior Developer",
  "company": "Tech Corp",
  "location": "Remote",
  "description": "Job description...",
  "employment_type": "Full-time",
  "tech_skills": ["Python", "React"],
  "soft_skills": ["communication"],
  "seniority": "senior",
  "salary_min": 5000,
  "salary_max": 8000
}
```

#### **4. Update Job**

```http
PUT /api/v1/jobs/{job_id}
Content-Type: application/json

{
  "status": "analyzed",
  "salary": "$6,000-8,000"
}
```

#### **5. Delete Job**

```http
DELETE /api/v1/jobs/{job_id}
```

#### **6. Search Jobs**

```http
GET /api/v1/jobs/search?q=developer&company=Gamma&seniority=mid
```

**Query Parameters:**

- `q`: Search query (title, description)
- `company`: Company name filter
- `seniority`: Seniority level filter
- `type`: Job type filter (remote/hybrid/onsite)
- `tech_skills`: Tech skills filter
- `salary_min`: Minimum salary filter

---

### **🤖 Scraped Jobs APIs**

#### **1. Bulk Import Scraped Jobs**

```http
POST /api/v1/scraped-jobs/import
Content-Type: application/json

{
  "jobs": [
    {
      "data": {
        "company": "Gamma",
        "title": "Full Stack Developer",
        "location": "Remote",
        "salary": "$2,500+",
        "tech_skills": ["React.js", "Node.js"],
        "soft_skills": ["communication"],
        "description": "Job description...",
        "employment_type": "Full-time",
        "job_link": "https://example.com/job",
        "seniority": "Mid",
        "scraped_at": "Sun, 17 Aug 2025 00:02:43 GMT",
        "updated_at": "Sun, 17 Aug 2025 00:02:43 GMT",
        "date_posted": "Not specified"
      },
      "success": true,
      "message": "Job scraped successfully",
      "scraped_at": "2025-08-17T00:02:43.608904"
    }
  ]
}
```

**Response:**

```json
{
  "total_jobs": 1,
  "successful_imports": 1,
  "failed_imports": 0,
  "created_jobs": ["68a133c8b639eadc6cfd5b73"],
  "updated_jobs": [],
  "errors": [],
  "message": "Successfully imported all 1 jobs"
}
```

#### **2. Single Job Import**

```http
POST /api/v1/scraped-jobs/import/single
```

#### **3. Scraping Statistics**

```http
GET /api/v1/scraped-jobs/stats
```

**Response:**

```json
{
  "total_jobs": 3,
  "scraped_jobs": 3,
  "manual_jobs": 0,
  "recently_scraped": 3,
  "scraping_coverage": 100.0
}
```

---

### **📊 Analytics APIs**

#### **1. Dashboard Statistics**

```http
GET /api/v1/analytics/dashboard
```

**Expected Response:**

```json
{
  "total_jobs": 3,
  "applications_this_week": 2,
  "response_rate": 0.33,
  "avg_response_time": 5.5,
  "status_distribution": {
    "new": 3,
    "analyzed": 0,
    "matched": 0,
    "closed": 0
  },
  "seniority_distribution": {
    "junior": 0,
    "mid": 2,
    "senior": 1
  },
  "type_distribution": {
    "remote": 2,
    "hybrid": 1,
    "onsite": 0
  }
}
```

#### **2. Skills Analytics**

```http
GET /api/v1/analytics/skills
```

**Expected Response:**

```json
{
  "top_tech_skills": [
    { "skill": "React.js", "count": 2, "percentage": 66.7 },
    { "skill": "Node.js", "count": 2, "percentage": 66.7 },
    { "skill": "Python", "count": 1, "percentage": 33.3 }
  ],
  "top_soft_skills": [
    { "skill": "communication", "count": 3, "percentage": 100.0 },
    { "skill": "teamwork", "count": 2, "percentage": 66.7 },
    { "skill": "leadership", "count": 1, "percentage": 33.3 }
  ],
  "trending_skills": ["React.js", "TypeScript", "Docker"]
}
```

#### **3. Application Timeline**

```http
GET /api/v1/analytics/timeline?period=30
```

---

## 🎯 **Frontend Data Requirements**

### **📊 Dashboard Components**

#### **1. Job Cards Display**

**Data needed:**

```javascript
{
  id: "68a133c8b639eadc6cfd5b73",
  title: "Full Stack Developer - IC",
  company: "Gamma",
  location: "Remote",
  salary: "$2,500+",
  employment_type: "Full-time",
  job_link: "https://...",
  tech_skills: ["React.js", "Next.js", "Node.js"],
  soft_skills: ["communication", "leadership"],
  seniority: "mid",
  type: "remote",
  scraped_at: "2025-08-17T01:43:36.748Z",
  status: "new"
}
```

#### **2. Skills Visualization**

**Tech Skills Chart:**

```javascript
{
  labels: ["React.js", "Node.js", "Python", "TypeScript"],
  data: [2, 2, 1, 1],
  percentages: [66.7, 66.7, 33.3, 33.3]
}
```

**Soft Skills Chart:**

```javascript
{
  labels: ["communication", "teamwork", "leadership"],
  data: [3, 2, 1],
  percentages: [100.0, 66.7, 33.3]
}
```

#### **3. Seniority Distribution**

```javascript
{
  "Junior": 0,
  "Mid": 2,
  "Senior": 1
}
```

#### **4. Location Type Distribution**

```javascript
{
  "Remote": 2,
  "Hybrid": 1,
  "Onsite": 0
}
```

#### **5. Scraping Coverage Metrics**

```javascript
{
  total_jobs: 3,
  scraped_jobs: 3,
  manual_jobs: 0,
  coverage: 100.0,
  recently_scraped: 3
}
```

---

### **🔍 Filter Options**

**Company Filter:**

```javascript
["Gamma", "TechStartup Inc", "CloudTech Solutions"];
```

**Seniority Filter:**

```javascript
["junior", "mid", "senior"];
```

**Type Filter:**

```javascript
["remote", "hybrid", "onsite"];
```

**Tech Skills Filter:**

```javascript
[
  "React.js",
  "Next.js",
  "Node.js",
  "Python",
  "TypeScript",
  "PostgreSQL",
  "Redux",
];
```

**Employment Type Filter:**

```javascript
["Full-time", "Part-time", "Contract", "Freelance"];
```

---

### **🎨 Frontend Display Examples**

#### **Job Card Template:**

```jsx
<JobCard>
  <Title>{job.title}</Title>
  <Company>{job.company}</Company>
  <Location>
    {job.location} • {job.employment_type}
  </Location>
  <Salary>{job.salary}</Salary>

  <SkillsSection>
    <TechSkills>
      {job.tech_skills.map((skill) => (
        <SkillTag key={skill} type="tech">
          {skill}
        </SkillTag>
      ))}
    </TechSkills>
    <SoftSkills>
      {job.soft_skills.map((skill) => (
        <SkillTag key={skill} type="soft">
          {skill}
        </SkillTag>
      ))}
    </SoftSkills>
  </SkillsSection>

  <Footer>
    <SeniorityBadge>{job.seniority}</SeniorityBadge>
    <TypeBadge>{job.type}</TypeBadge>
    {job.scraped_at && <ScrapedIndicator />}
    <ApplyButton href={job.job_link}>Apply</ApplyButton>
  </Footer>
</JobCard>
```

#### **Analytics Dashboard:**

```jsx
<Dashboard>
  <MetricsRow>
    <Metric value={stats.total_jobs} label="Total Jobs" />
    <Metric value={stats.scraped_jobs} label="Scraped Jobs" />
    <Metric value={`${stats.scraping_coverage}%`} label="Coverage" />
  </MetricsRow>

  <ChartsRow>
    <SkillsChart data={techSkillsData} title="Top Tech Skills" />
    <SeniorityChart data={seniorityData} title="Seniority Levels" />
    <LocationChart data={locationData} title="Job Types" />
  </ChartsRow>
</Dashboard>
```

---

## ⚡ **Quick Setup Commands**

```bash
# 1. Start MongoDB (if not running)
sudo systemctl start mongod

# 2. Start Backend Server
cd server
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000

# 3. Test APIs
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/jobs
curl http://localhost:8000/api/v1/scraped-jobs/stats

# 4. View API Documentation
# Open: http://localhost:8000/docs
```

---

## 🎯 **Next Steps for Frontend**

1. **Update job cards** to display new fields (`employment_type`, `job_link`, etc.)
2. **Separate tech and soft skills** in the UI
3. **Add scraping indicators** for jobs imported from scraper
4. **Implement salary display** (both string and numeric ranges)
5. **Add apply buttons** linking to `job_link`
6. **Create scraping dashboard** showing import statistics
7. **Add filters** for new fields (employment_type, etc.)

**Your MongoDB collections and APIs are ready for the enhanced frontend! 🚀**
