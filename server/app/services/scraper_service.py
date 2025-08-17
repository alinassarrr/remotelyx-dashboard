"""
Job Scraper Service
Core job scraping functionality with AI-powered extraction
"""
import json
import re
import ollama
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from ..core.config import get_settings
from ..core.database import get_collection

logger = logging.getLogger(__name__)

class BrowserManager:
    """Manages Chrome browser setup and configuration"""
    
    @staticmethod
    def get_chrome_options() -> Options:
        """Get optimized Chrome options for web scraping"""
        options = Options()
        browser_options = [
            '--headless',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--window-size=1920,1080',
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        for option in browser_options:
            options.add_argument(option)
        return options
    
    @staticmethod
    def create_driver() -> Optional[webdriver.Chrome]:
        """Create and return a Chrome driver instance"""
        try:
            options = BrowserManager.get_chrome_options()
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            return None


class AIDataExtractor:
    """AI-powered job data extraction using Ollama"""
    
    @staticmethod
    def extract_job_data(html_content: str, url: str) -> Dict[str, Any]:
        """Extract job data using AI analysis"""
        
        # Clean and prepare the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get clean text content
        text_content = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text_content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Truncate if too long
        if len(clean_text) > 8000:
            clean_text = clean_text[:8000] + "..."
        
        # Enhanced AI prompt for better extraction
        prompt = f"""
        You are an expert job data extraction AI. Analyze this job posting and extract comprehensive information.

        CRITICAL REQUIREMENTS:
        - Extract ALL technical and soft skills mentioned
        - Write a detailed 200-400 word description
        - Find salary information (look for numbers, ranges, "k", "$")
        - NEVER leave skills arrays empty

        Return ONLY this JSON format:

        {{
            "title": "exact job title from posting",
            "company": "company name (look for company references)",
            "location": "job location or Remote",
            "employment_type": "Full-time/Part-time/Contract/Internship",
            "salary": "salary amount like 50000$ or 40000$-60000$ or Not specified",
            "date_posted": "{datetime.now().strftime('%Y-%m-%d')}",
            "description": "comprehensive description covering role, responsibilities, requirements, company info, benefits",
            "tech_skills": ["extract ALL: languages like Python,JavaScript,Java; frameworks like React,Angular; tools like Docker,AWS,Git; databases like MySQL,MongoDB"],
            "soft_skills": ["extract ALL: communication, teamwork, leadership, problem-solving, creativity, time-management, adaptability"],
            "seniority": "Junior/Mid/Senior based on experience required",
            "job_link": "{url}"
        }}

        EXTRACTION RULES:
        1. TECH SKILLS: Find programming languages, frameworks, databases, cloud services, tools, methodologies
        2. SOFT SKILLS: Find communication, leadership, teamwork, problem-solving, creativity, organization skills
        3. SALARY: Look for $, numbers, "k", salary ranges, compensation mentions
        4. DESCRIPTION: Write 200-400 words covering role overview, key responsibilities, requirements, company info
        5. If no skills found explicitly, infer from job requirements and responsibilities

        Job posting content:
        {clean_text}

        Extract everything thoroughly. Return ONLY the JSON.
        """
        
        try:
            # Use FREE Ollama local AI
            response = ollama.chat(
                model="llama3.2",
                messages=[
                    {"role": "system", "content": "You are a job data extraction expert. Always return valid JSON with complete data."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract and parse the response
            ai_response = response['message']['content'].strip()
            
            # Clean response (remove markdown formatting if present)
            if ai_response.startswith("```json"):
                ai_response = ai_response[7:-3]
            elif ai_response.startswith("```"):
                ai_response = ai_response[3:-3]
            
            # Parse JSON
            job_data = json.loads(ai_response)
            
            # Validate that required fields have content
            if not job_data.get('tech_skills') or len(job_data.get('tech_skills', [])) == 0:
                job_data['tech_skills'] = AIDataExtractor._extract_fallback_skills(clean_text, 'tech')
            
            if not job_data.get('soft_skills') or len(job_data.get('soft_skills', [])) == 0:
                job_data['soft_skills'] = AIDataExtractor._extract_fallback_skills(clean_text, 'soft')
            
            if not job_data.get('description') or len(job_data.get('description', '')) < 50:
                job_data['description'] = AIDataExtractor._extract_fallback_description(clean_text)
            
            if not job_data.get('salary') or job_data.get('salary') == 'Not specified':
                job_data['salary'] = AIDataExtractor._extract_fallback_salary(clean_text)
            
            return job_data
            
        except Exception as e:
            logger.error(f"AI extraction failed: {e}")
            # Fallback to basic extraction
            return AIDataExtractor._fallback_extraction(clean_text, url)
    
    @staticmethod
    def _extract_fallback_skills(text: str, skill_type: str) -> List[str]:
        """Extract skills using keyword matching as fallback"""
        text_lower = text.lower()
        
        if skill_type == 'tech':
            tech_keywords = [
                'python', 'javascript', 'java', 'react', 'node.js', 'angular', 'vue', 'typescript',
                'html', 'css', 'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'aws', 'azure',
                'docker', 'kubernetes', 'git', 'linux', 'php', 'ruby', 'go', 'rust', 'c++', 'c#',
                'terraform', 'jenkins', 'api', 'rest', 'graphql', 'microservices', 'devops'
            ]
            found_skills = []
            for skill in tech_keywords:
                if skill in text_lower:
                    found_skills.append(skill.title())
            return found_skills[:10]  # Limit to 10 skills
        
        elif skill_type == 'soft':
            soft_keywords = [
                'communication', 'leadership', 'teamwork', 'problem-solving', 'adaptability',
                'creativity', 'time management', 'organization', 'collaboration', 'mentoring',
                'project management', 'agile', 'customer service', 'analytical thinking',
                'critical thinking', 'attention to detail', 'multitasking'
            ]
            found_skills = []
            for skill in soft_keywords:
                if skill in text_lower:
                    found_skills.append(skill.title())
            return found_skills[:8]  # Limit to 8 skills
        
        return []
    
    @staticmethod
    def _extract_fallback_description(text: str) -> str:
        """Extract a comprehensive description as fallback"""
        # Clean and create a description from the content
        lines = text.split('\n')
        description_parts = []
        
        for line in lines:
            line = line.strip()
            if len(line) > 20 and not line.isupper():
                description_parts.append(line)
        
        full_description = ' '.join(description_parts)
        
        # Limit to reasonable length
        if len(full_description) > 500:
            full_description = full_description[:500] + "..."
        
        return full_description if full_description else "Job description not available."
    
    @staticmethod
    def _extract_fallback_salary(text: str) -> str:
        """Extract salary information as fallback"""
        # Look for salary patterns
        salary_patterns = [
            r'\$(\d{1,3}(?:,\d{3})*)',
            r'(\d{2,3})k',
            r'(\d{2,3})[kK]',
            r'salary.*?\$?(\d{1,3}(?:,\d{3})*)',
            r'compensation.*?\$?(\d{1,3}(?:,\d{3})*)',
        ]
        
        for pattern in salary_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Process the first match
                match = matches[0]
                if 'k' in text.lower() and len(match) <= 3:
                    return f"{int(match) * 1000}$"
                elif match.replace(',', '').isdigit():
                    return f"{match}$"
        
        return "Not specified"
    
    @staticmethod
    def _fallback_extraction(text: str, url: str) -> Dict[str, Any]:
        """Fallback extraction method if AI fails"""
        # Simple regex-based extraction as fallback
        title_match = re.search(r'(?:position|role|job):\s*([^\n]+)', text, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else "Job Position"
        
        company_match = re.search(r'(?:company|organization):\s*([^\n]+)', text, re.IGNORECASE)
        company = company_match.group(1).strip() if company_match else "Company"
        
        return {
            "title": title,
            "company": company,
            "location": "Not specified",
            "employment_type": "Full-time",
            "salary": AIDataExtractor._extract_fallback_salary(text),
            "date_posted": datetime.now().strftime('%Y-%m-%d'),
            "description": AIDataExtractor._extract_fallback_description(text),
            "tech_skills": AIDataExtractor._extract_fallback_skills(text, 'tech'),
            "soft_skills": AIDataExtractor._extract_fallback_skills(text, 'soft'),
            "seniority": "Mid",
            "job_link": url
        }


class JobScraperService:
    """Main scraper service for job postings"""
    
    def __init__(self):
        self.driver = None
        self.settings = get_settings()
        self.jobs_collection = get_collection("jobs")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
    
    def setup_driver(self) -> bool:
        """Setup Chrome driver"""
        self.driver = BrowserManager.create_driver()
        return self.driver is not None
    
    def cleanup(self):
        """Clean up browser resources"""
        if self.driver:
            self.driver.quit()
    
    def fetch_job_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch job page using Selenium"""
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            
            # Wait for page to load
            import time
            time.sleep(3)
            
            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            
            return soup
            
        except Exception as e:
            logger.error(f"Error fetching page: {e}")
            return None
    
    async def scrape_job(self, url: str) -> Optional[Dict[str, Any]]:
        """Main scraping function with AI-powered extraction"""
        if not self.setup_driver():
            return None
        
        try:
            soup = self.fetch_job_page(url)
            if not soup:
                return None
            
            logger.info("Using AI-powered extraction...")
            try:
                ai_extractor = AIDataExtractor()
                job_data = ai_extractor.extract_job_data(self.driver.page_source, url)
                logger.info("AI extraction successful!")
                return job_data
            except Exception as e:
                logger.error(f"AI extraction failed: {e}")
                return None
            
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            return None
        finally:
            self.cleanup()
    
    async def scrape_and_save_job(self, url: str) -> Dict[str, Any]:
        """Scrape job and save to database"""
        job_data = await self.scrape_job(url)
        if not job_data:
            raise ValueError("Failed to scrape job data")
        
        # Check for duplicates
        existing_job = await self.jobs_collection.find_one({"job_link": url})
        if existing_job:
            logger.info(f"Job already exists: {url}")
            return job_data
        
        # Save to database
        job_data["created_at"] = datetime.now()
        result = await self.jobs_collection.insert_one(job_data)
        job_data["_id"] = str(result.inserted_id)
        
        logger.info(f"Job saved successfully: {job_data['title']} at {job_data['company']}")
        return job_data
    
    async def get_recent_jobs(self, limit: int = 10, skip: int = 0) -> List[Dict[str, Any]]:
        """Get recent jobs from database"""
        cursor = self.jobs_collection.find().sort("created_at", -1).skip(skip).limit(limit)
        jobs = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string for JSON serialization
        for job in jobs:
            job["_id"] = str(job["_id"])
        
        return jobs
    
    async def get_job_stats(self) -> Dict[str, Any]:
        """Get job scraping statistics"""
        total_jobs = await self.jobs_collection.count_documents({})
        
        # Jobs added today
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        jobs_today = await self.jobs_collection.count_documents({
            "created_at": {"$gte": today}
        })
        
        return {
            "total_jobs": total_jobs,
            "jobs_today": jobs_today,
            "last_updated": datetime.now().isoformat()
        }
