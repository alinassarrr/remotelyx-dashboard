from typing import List
from datetime import datetime, timedelta
from app.services.job_service import JobService
from app.models.job import JobCreate, JobData
import logging
import random

logger = logging.getLogger(__name__)

class SeederService:
    def __init__(self):
        self.job_service = JobService()
    
    async def seed_sample_jobs(self, count: int = 50) -> List[str]:
        """Seed the database with sample job data."""
        try:
            logger.info(f"Starting to seed {count} sample jobs...")
            
            # Sample data for generating realistic jobs
            companies = [
                "TechCorp", "StartupXYZ", "Enterprise Solutions", "Innovation Labs", 
                "Digital Dynamics", "CloudBase", "DataWorks", "CyberSec Pro", 
                "DevOps Hub", "Productify", "Creative Studios", "Analytics Pro",
                "Mobile First", "AI Ventures", "Blockchain Tech", "Green Energy Co",
                "HealthTech", "FinTech Solutions", "EduTech", "Retail Innovations"
            ]
            
            locations = [
                "Remote", "New York, NY", "San Francisco, CA", "Austin, TX", 
                "Seattle, WA", "Boston, MA", "Denver, CO", "Chicago, IL",
                "Los Angeles, CA", "Miami, FL", "Portland, OR", "Atlanta, GA",
                "Toronto, Canada", "London, UK", "Berlin, Germany", "Amsterdam, Netherlands"
            ]
            
            employment_types = [
                "Full-time", "Part-time", "Contract", "Freelance", "Internship"
            ]
            
            seniority_levels = [
                "Junior", "Mid", "Senior", "Lead", "Principal", "Executive"
            ]
            
            tech_skills = [
                "JavaScript", "Python", "React", "Node.js", "Java", "C++", "C#", "Go",
                "TypeScript", "Vue.js", "Angular", "Django", "Flask", "Spring Boot",
                "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Terraform",
                "MongoDB", "PostgreSQL", "MySQL", "Redis", "Elasticsearch",
                "Machine Learning", "Data Analysis", "Statistics", "R", "TensorFlow",
                "PyTorch", "Git", "CI/CD", "Jenkins", "GitHub Actions", "Linux",
                "Shell Scripting", "REST APIs", "GraphQL", "Microservices"
            ]
            
            soft_skills = [
                "Communication", "Leadership", "Teamwork", "Problem Solving",
                "Critical Thinking", "Adaptability", "Time Management", "Creativity",
                "Analytical Skills", "Customer Focus", "Collaboration", "Innovation",
                "Strategic Thinking", "Decision Making", "Conflict Resolution"
            ]
            
            job_titles = [
                "Software Engineer", "Full Stack Developer", "Frontend Developer", 
                "Backend Developer", "DevOps Engineer", "Data Scientist", 
                "Machine Learning Engineer", "Product Manager", "UX Designer",
                "UI Designer", "Data Engineer", "Site Reliability Engineer",
                "Security Engineer", "Mobile Developer", "QA Engineer",
                "Technical Lead", "Engineering Manager", "Solutions Architect"
            ]
            
            salary_ranges = [
                "$40k - $60k", "$60k - $80k", "$80k - $100k", "$100k - $120k",
                "$120k - $150k", "$150k+", "$2,500+", "$3,000+", "$4,000+",
                "$5,000+", "$6,000+", "$8,000+", "$10,000+"
            ]
            
            # Generate sample jobs
            sample_jobs = []
            for i in range(count):
                # Randomize job data
                company = random.choice(companies)
                location = random.choice(locations)
                employment_type = random.choice(employment_types)
                seniority = random.choice(seniority_levels)
                title = random.choice(job_titles)
                
                # Generate random skills (3-8 tech skills, 2-5 soft skills)
                num_tech_skills = random.randint(3, 8)
                num_soft_skills = random.randint(2, 5)
                
                job_tech_skills = random.sample(tech_skills, num_tech_skills)
                job_soft_skills = random.sample(soft_skills, num_soft_skills)
                
                # Generate random dates (within last 30 days)
                days_ago = random.randint(0, 30)
                created_date = datetime.utcnow() - timedelta(days=days_ago)
                
                # Create job data
                job_data = JobData(
                    company=company,
                    date_posted=f"{days_ago} days ago",
                    description=f"We are looking for a {seniority.lower()} {title.lower()} to join our dynamic team at {company}. This is an exciting opportunity to work on cutting-edge projects and grow your career.",
                    employment_type=employment_type,
                    job_link=f"https://example.com/jobs/{i+1}",
                    location=location,
                    salary=random.choice(salary_ranges),
                    scraped_at=created_date.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                    seniority=seniority,
                    soft_skills=job_soft_skills,
                    tech_skills=job_tech_skills,
                    title=title,
                    updated_at=created_date.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                    status=random.choice(["New", "Analyzed", "Matched", "In Progress"])
                )
                
                # Create job object
                job = JobCreate(
                    data=job_data,
                    message=f"Job created successfully (ID: {i+1})",
                    scraped_at=created_date.isoformat(),
                    success=True
                )
                
                sample_jobs.append(job)
            
            # Bulk create jobs
            job_ids = await self.job_service.bulk_create_jobs(sample_jobs)
            
            logger.info(f"Successfully seeded {len(job_ids)} sample jobs")
            return job_ids
            
        except Exception as e:
            logger.error(f"Error seeding sample jobs: {e}")
            raise e
    
    async def seed_n8n_format_jobs(self, jobs_data: List[dict]) -> List[str]:
        """Seed jobs from n8n scraper format."""
        try:
            logger.info(f"Starting to seed {len(jobs_data)} jobs from n8n format...")
            
            # Convert n8n format to our models
            jobs_to_create = []
            for job_data in jobs_data:
                try:
                    # Extract the job data from n8n format
                    if "data" in job_data:
                        n8n_job_data = job_data["data"]
                        
                        # Create JobData object
                        job_data_obj = JobData(
                            company=n8n_job_data.get("company", "Unknown Company"),
                            date_posted=n8n_job_data.get("date_posted", "Not specified"),
                            description=n8n_job_data.get("description", ""),
                            employment_type=n8n_job_data.get("employment_type", "Full-time"),
                            job_link=n8n_job_data.get("job_link", ""),
                            location=n8n_job_data.get("location", "Remote"),
                            salary=n8n_job_data.get("salary", "Not specified"),
                            scraped_at=n8n_job_data.get("scraped_at", ""),
                            seniority=n8n_job_data.get("seniority", "Mid"),
                            soft_skills=n8n_job_data.get("soft_skills", []),
                            tech_skills=n8n_job_data.get("tech_skills", []),
                            title=n8n_job_data.get("title", "Job Title"),
                            updated_at=n8n_job_data.get("updated_at", ""),
                            status=n8n_job_data.get("status", "New")
                        )
                        
                        # Create JobCreate object
                        job = JobCreate(
                            data=job_data_obj,
                            message=job_data.get("message", "Job created successfully"),
                            scraped_at=job_data.get("scraped_at", ""),
                            success=job_data.get("success", True)
                        )
                        
                        jobs_to_create.append(job)
                        
                except Exception as e:
                    logger.warning(f"Failed to process job data: {e}")
                    continue
            
            if jobs_to_create:
                # Bulk create jobs
                job_ids = await self.job_service.bulk_create_jobs(jobs_to_create)
                logger.info(f"Successfully seeded {len(job_ids)} jobs from n8n format")
                return job_ids
            else:
                logger.warning("No valid jobs to create from n8n format")
                return []
                
        except Exception as e:
            logger.error(f"Error seeding n8n format jobs: {e}")
            raise e
    
    async def clear_all_jobs(self) -> bool:
        """Clear all jobs from the database."""
        try:
            logger.info("Clearing all jobs from database...")
            
            # Get the collection and delete all documents
            collection = self.job_service.collection
            result = await collection.delete_many({})
            
            logger.info(f"Cleared {result.deleted_count} jobs from database")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing jobs: {e}")
            raise e
    
    async def get_seeding_status(self) -> dict:
        """Get the current status of the database."""
        try:
            total_jobs = await self.job_service.collection.count_documents({})
            
            # Get some sample data for verification
            sample_jobs = await self.job_service.collection.find().limit(5).to_list(5)
            
            return {
                "total_jobs": total_jobs,
                "has_data": total_jobs > 0,
                "sample_jobs_count": len(sample_jobs),
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting seeding status: {e}")
            raise e 