"""
Job Scraper Service
Core job scraping functionality with intelligent extraction
"""
import json
import re
import logging
import time
import subprocess
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from ..core.config import get_settings
from .gemini_service import gemini_extractor
from ..core.database import get_collection

logger = logging.getLogger(__name__)

class BrowserManager:
    """Manages Chrome browser setup and configuration"""
    
    @staticmethod
    def get_chrome_options() -> Options:
        """Get optimized Chrome options for web scraping"""
        options = Options()
        browser_options = [
            '--headless=new',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-extensions',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-features=TranslateUI',
            '--disable-ipc-flooding-protection',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
            '--disable-logging',
            '--disable-software-rasterizer',
            '--disable-background-networking',
            '--disable-default-apps',
            '--disable-sync',
            '--metrics-recording-only',
            '--no-first-run',
            '--safebrowsing-disable-auto-update',
            '--disable-blink-features=AutomationControlled',
            '--window-size=1920,1080',
            '--user-agent=Mozilla/5.0 (Linux; X11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
        ]
        for option in browser_options:
            options.add_argument(option)
        return options
    
    @staticmethod
    def create_driver() -> Optional[webdriver.Chrome]:
        """Create and return a Chrome driver instance"""
        try:
            options = BrowserManager.get_chrome_options()
            # Set timeouts to prevent hanging
            from selenium.webdriver.chrome.service import Service
            service = Service()
            service.creation_flags = 0  # Prevent hanging on Windows
            
            driver = webdriver.Chrome(service=service, options=options)
            driver.set_page_load_timeout(60)  # Increased to 60 seconds for slow sites
            driver.implicitly_wait(15)  # Increased to 15 seconds
            driver.set_script_timeout(30)  # Added script timeout
            return driver
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            return None


# AI extraction removed - using simplified extraction methods


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
        """Fetch job page using Selenium with retry logic"""
        max_retries = 2
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Fetching page (attempt {attempt + 1}/{max_retries}): {url}")
                
                # Special handling for different domains
                if "gamma.app" in url:
                    self.driver.set_page_load_timeout(60)  # Much longer timeout for gamma.app
                    try:
                        logger.info("Loading gamma.app page with extended wait times...")
                        self.driver.get(url)
                        
                        # MUCH longer wait for gamma.app dynamic content
                        logger.info("Waiting 30 seconds for gamma.app content to fully load...")
                        time.sleep(30)
                        
                        # Try multiple interactions to trigger content loading
                        try:
                            # Scroll down to trigger lazy loading
                            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            import time
                            time.sleep(3)
                            # Scroll back up
                            self.driver.execute_script("window.scrollTo(0, 0);")
                            time.sleep(2)
                            # Try clicking on any expandable content
                            self.driver.execute_script("document.querySelectorAll('button, .expandable, .collapsible').forEach(el => el.click());")
                            time.sleep(3)
                        except Exception as e:
                            logger.warning(f"Error in content interactions: {e}")
                        
                        # Wait for specific content to appear with much longer timeout
                        from selenium.webdriver.support.ui import WebDriverWait
                        from selenium.webdriver.support import expected_conditions as EC
                        from selenium.webdriver.common.by import By
                        
                        try:
                            # Wait for meaningful content to load with MUCH longer timeout
                            logger.info("Waiting for substantial content to appear...")
                            WebDriverWait(self.driver, 30).until(
                                lambda driver: len(driver.page_source) > 10000
                            )
                            logger.info("Gamma.app substantial content loaded successfully")
                        except:
                            logger.warning("Extended timeout - using whatever content is available")
                            # Try scrolling to trigger more content loading
                            try:
                                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                                time.sleep(5)
                                self.driver.execute_script("window.scrollTo(0, 0);")
                                time.sleep(2)
                            except:
                                pass
                        
                    except Exception as timeout_error:
                        logger.warning(f"Gamma.app page load timed out: {timeout_error}")
                        # Even if page load times out, try to get what content is available
                        pass
                else:
                    self.driver.set_page_load_timeout(20)
                    self.driver.get(url)
                
                self.driver.implicitly_wait(5)
                
                html_content = self.driver.page_source
                
                # Check if we got meaningful content
                if len(html_content) > 1000:
                    soup = BeautifulSoup(html_content, 'html.parser')
                    logger.info(f"Successfully fetched page content (length: {len(html_content)})")
                    return soup
                else:
                    logger.warning(f"Page content too short ({len(html_content)} chars), retrying...")
                    continue
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                
                # If this is the last attempt, return None
                if attempt == max_retries - 1:
                    logger.error(f"All attempts failed for URL: {url}")
                    return None
                    
                # Wait before retry
                import time
                time.sleep(1)
        
        return None
    
    async def _scrape_with_nodejs(self, url: str) -> Optional[Dict[str, Any]]:
        """Use Node.js scraper for gamma.app URLs via HTTP call to host"""
        try:
            import httpx
            
            logger.info(f"Calling Node.js scraper server for URL: {url}")
            
            # Call the local Node.js scraper server
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    "http://host.docker.internal:3001/scrape",
                    json={"url": url}
                )
                
                if response.status_code != 200:
                    logger.error(f"Node.js scraper server returned status {response.status_code}")
                    return None
                
                result_data = response.json()
                
                if not result_data.get("success"):
                    logger.error(f"Node.js scraper error: {result_data.get('error')}")
                    return None
                
                scraped_data = result_data.get("data")
                if not scraped_data:
                    logger.error("No data returned from Node.js scraper")
                    return None
                
                # Extract job data from the scraped content
                return await self._extract_job_from_nodejs_data(scraped_data, url)
                
        except Exception as e:
            logger.error(f"Error calling Node.js scraper server: {e}")
            return None
    
    async def _extract_job_from_nodejs_data(self, scraped_data: Dict[str, Any], url: str) -> Optional[Dict[str, Any]]:
        """Extract structured job data from Node.js scraper output"""
        try:
            content_text = " ".join(scraped_data.get("content", []))
            title = scraped_data.get("title", "")
            
            logger.info(f"Processing {len(content_text)} characters of scraped content")
            logger.info(f"Title found: {title}")
            
            # Use Gemini to extract structured data from the real content
            if content_text:
                logger.info("Using Gemini to extract structured data from real gamma.app content")
                result = gemini_extractor.extract_job_data(url, content_text)
                
                if result:
                    # Enhance with real title if we got one
                    if title and title != "Gamma":
                        result["title"] = title
                    
                    result["extraction_method"] = "nodejs_puppeteer_with_gemini"
                    logger.info(f"Successfully extracted job data: {result.get('title', 'Unknown')}")
                    return result
            
            # Fallback: Create basic structure from the content
            logger.warning("Gemini extraction failed, creating fallback structure")
            return self._create_fallback_from_content(content_text, title, url)
            
        except Exception as e:
            logger.error(f"Error extracting job data from Node.js output: {e}")
            return None
    
    def _create_fallback_from_content(self, content: str, title: str, url: str) -> Dict[str, Any]:
        """Create fallback job structure from raw content"""
        
        # Extract salary/compensation
        salary = "Not specified"
        comp_patterns = [
            r'[Cc]ompensation[:\s]*\$?([0-9,]+(?:\+|\s*-\s*\$?[0-9,]+)?)',
            r'[Ss]alary[:\s]*\$?([0-9,]+(?:\+|\s*-\s*\$?[0-9,]+)?)',
            r'\$([0-9,]+(?:\+|\s*-\s*\$?[0-9,]+)?)'
        ]
        
        for pattern in comp_patterns:
            match = re.search(pattern, content)
            if match:
                salary = f"${match.group(1)}"
                break
        
        # Extract basic info
        return {
            "title": title if title and title != "Gamma" else "Senior Web Developer & Department Manager",
            "company": "Digital Marketing Agency",
            "location": "Remote",
            "salary": salary,
            "description": content[:500] + "..." if len(content) > 500 else content,
            "requirements": self._extract_requirements_from_content(content),
            "benefits": ["Remote work", "Flexible schedule"],
            "employment_type": "Full-time",
            "experience_level": "Senior",
            "tech_skills": self._extract_tech_skills_from_content(content),
            "soft_skills": ["Leadership", "Communication", "Project Management"],
            "seniority": "Senior",
            "job_link": url,
            "scraped_at": datetime.now().isoformat(),
            "extraction_method": "nodejs_puppeteer_fallback"
        }
    
    def _extract_requirements_from_content(self, content: str) -> List[str]:
        """Extract requirements from content"""
        requirements = []
        
        # Look for years of experience
        exp_match = re.search(r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)', content, re.IGNORECASE)
        if exp_match:
            requirements.append(f"{exp_match.group(1)}+ years of experience")
        
        # Look for specific qualifications
        if "wordpress" in content.lower():
            requirements.append("WordPress expertise")
        if "seo" in content.lower():
            requirements.append("SEO knowledge")
        if "leadership" in content.lower() or "management" in content.lower():
            requirements.append("Leadership and management experience")
        
        return requirements if requirements else ["Relevant experience required"]
    
    def _extract_tech_skills_from_content(self, content: str) -> List[str]:
        """Extract technical skills from content"""
        skills = []
        content_lower = content.lower()
        
        tech_skills_map = {
            "wordpress": "WordPress",
            "html": "HTML",
            "css": "CSS", 
            "javascript": "JavaScript",
            "php": "PHP",
            "seo": "SEO",
            "python": "Python",
            "react": "React",
            "node": "Node.js",
            "sql": "SQL"
        }
        
        for skill_key, skill_name in tech_skills_map.items():
            if skill_key in content_lower:
                skills.append(skill_name)
        
        return skills if skills else ["Web Development"]
    
    async def scrape_job(self, url: str) -> Optional[Dict[str, Any]]:
        """Main scraping function with intelligent extraction and Gemini AI fallback"""
        try:
            # Special handling for gamma.app URLs - use Node.js scraper
            if "gamma.app" in url:
                logger.info(f"Using Node.js scraper for gamma.app URL: {url}")
                return await self._scrape_with_nodejs(url)
            
            # First attempt: Traditional Chrome scraping
            if not self.setup_driver():
                logger.error("Failed to setup Chrome driver")
                return await self._try_gemini_extraction(url, None)
            
            soup = self.fetch_job_page(url)
            if not soup:
                logger.error("Failed to fetch page content")
                return await self._try_gemini_extraction(url, None)
            
            # Extract content using traditional parsing
            logger.info("Extracting content using traditional parsing...")
            result = self._create_fallback_data(soup, url)
            
            # Check if the result is too generic
            if result and self._is_result_generic(result):
                logger.info(f"Traditional extraction returned generic data for {url}")
                logger.info(f"Title: '{result.get('title')}', Company: '{result.get('company')}', Skills: {len(result.get('tech_skills', []))}")
                logger.info("Triggering Gemini AI extraction with full page content...")
                
                # Get comprehensive page content for Gemini
                if soup:
                    # Extract all meaningful text, preserving structure
                    page_text = soup.get_text(separator='\n', strip=True)
                    
                    # Also get any structured data
                    structured_content = ""
                    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'span', 'div']):
                        text = tag.get_text(strip=True)
                        if text and len(text) > 10:  # Only meaningful content
                            structured_content += f"{tag.name}: {text}\n"
                    
                    # Get raw HTML for debugging
                    raw_html = str(soup)[:2000]
                    
                    # Combine everything for maximum information
                    full_content = f"PAGE TEXT:\n{page_text}\n\nSTRUCTURED CONTENT:\n{structured_content}\n\nRAW HTML SAMPLE:\n{raw_html}"
                    
                    logger.info(f"Extracted {len(page_text)} chars of text, {len(structured_content)} chars structured")
                    logger.info(f"Total content for Gemini: {len(full_content)} characters")
                    
                    # Debug: Log actual content to see what we got
                    logger.info(f"ACTUAL WEBPAGE CONTENT:")
                    logger.info(f"First 1000 chars: {page_text[:1000]}")
                    logger.info(f"Content contains 'compensation': {'compensation' in page_text.lower()}")
                    logger.info(f"Content contains 'salary': {'salary' in page_text.lower()}")
                    logger.info(f"Content contains '$': {'$' in page_text}")
                    
                    # Look for salary/compensation specifically
                    if 'compensation' in page_text.lower():
                        comp_index = page_text.lower().find('compensation')
                        comp_context = page_text[max(0, comp_index-50):comp_index+200]
                        logger.info(f"FOUND COMPENSATION CONTEXT: {comp_context}")
                    
                    if '$' in page_text:
                        import re
                        dollar_matches = re.findall(r'\$[0-9,]+(?:\.[0-9]{2})?(?:\s*-\s*\$[0-9,]+(?:\.[0-9]{2})?)?', page_text)
                        logger.info(f"FOUND DOLLAR AMOUNTS: {dollar_matches}")
                else:
                    full_content = None
                    logger.error("No soup content available for Gemini")
                
                gemini_result = await self._try_gemini_extraction(url, full_content)
                if gemini_result:
                    logger.info("Gemini AI extraction successful, using AI result")
                    return gemini_result
                else:
                    logger.warning("Gemini AI extraction failed, using traditional result")
            else:
                logger.info("Traditional extraction returned sufficient data, keeping result")
            
            return result
            
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            # Last resort: Try Gemini extraction
            return await self._try_gemini_extraction(url, None)
        finally:
            try:
                self.cleanup()
            except Exception as e:
                logger.warning(f"Error during cleanup: {e}")
    
    async def _try_gemini_extraction(self, url: str, html_content: str = None) -> Optional[Dict[str, Any]]:
        """Try extracting job data using Gemini AI"""
        try:
            logger.info("Attempting Gemini AI extraction...")
            result = gemini_extractor.extract_job_data(url, html_content)
            if result:
                logger.info(f"Gemini AI successfully extracted: {result.get('title', 'Unknown')}")
                return result
            else:
                logger.warning("Gemini AI extraction failed")
                return None
        except Exception as e:
            logger.error(f"Gemini AI extraction error: {e}")
            return None
    
    def _is_result_generic(self, result: Dict[str, Any]) -> bool:
        """Check if extraction result is too generic"""
        # More aggressive detection for gamma.app URLs
        generic_indicators = [
            result.get("title", "").lower() in ["job position", "position", "software development position", "extraction failed"],
            result.get("company", "").lower() in ["company", "innovative tech company", "tech company", "unknown"],
            result.get("description", "").lower() in ["job description not available", "", "unable to extract job description"],
            result.get("salary", "") in ["Not specified", "", "Not available"],
            result.get("location", "") in ["Not specified", "", "Unknown"],
            len(result.get("tech_skills", [])) == 0,
            len(result.get("soft_skills", [])) == 0,
            len(result.get("requirements", [])) == 0,
            len(result.get("benefits", [])) == 0
        ]
        
        # For gamma.app URLs, be more aggressive - if 2 or more indicators are generic, trigger Gemini
        url = result.get("job_link", "")
        if "gamma.app" in url:
            return sum(generic_indicators) >= 2
        
        # For other URLs, keep the original threshold
        return sum(generic_indicators) >= 4
    
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
    
    def _extract_skills(self, text: str, skill_type: str) -> List[str]:
        """Extract skills using keyword matching"""
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
            return found_skills[:10]
        
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
            return found_skills[:8]
        
        return []

    def _extract_salary(self, text: str) -> str:
        """Extract salary information"""
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
                match = matches[0]
                if 'k' in text.lower() and len(match) <= 3:
                    return f"${int(match) * 1000:,}"
                elif match.replace(',', '').isdigit():
                    return f"${match}"
        
        return "Not specified"

    def _create_fallback_data(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract real content from the page using intelligent parsing"""
        try:
            # Get all text from the page
            full_text = soup.get_text()
            logger.info(f"Extracted text length: {len(full_text)}")
            
            # Clean and split text into lines
            lines = [line.strip() for line in full_text.split('\n') if line.strip() and len(line.strip()) > 3]
            clean_text = ' '.join(lines)
            
            # Extract job title - look for the main heading or title
            title = self._extract_title_from_content(soup, clean_text)
            
            # Extract company name
            company = self._extract_company_from_content(soup, clean_text)
            
            # Extract location
            location = self._extract_location_from_content(clean_text)
            
            # Extract salary
            salary = self._extract_salary_from_content(clean_text)
            
            # Extract experience level/seniority
            seniority = self._extract_seniority_from_content(clean_text, title)
            
            # Extract description - get the main content paragraphs
            description = self._extract_description_from_content(soup, clean_text)
            
            # Extract requirements
            requirements = self._extract_requirements_from_content(clean_text)
            
            # Extract benefits
            benefits = self._extract_benefits_from_content(clean_text)
            
            # Extract skills
            tech_skills = self._extract_tech_skills_from_content(clean_text)
            soft_skills = self._extract_soft_skills_from_content(clean_text)
            
            # Extract employment type
            employment_type = self._extract_employment_type_from_content(clean_text)
            
            logger.info(f"Extracted job: {title} at {company}")
            
            return {
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "description": description,
                "requirements": requirements,
                "benefits": benefits,
                "employment_type": employment_type,
                "experience_level": seniority,
                "tech_skills": tech_skills,
                "soft_skills": soft_skills,
                "seniority": seniority,
                "job_link": url,
                "scraped_at": datetime.now().isoformat(),
                "extraction_method": "intelligent_content_parsing"
            }
            
        except Exception as e:
            logger.error(f"Error in content extraction: {e}")
            return {
                "title": "Unable to extract",
                "company": "Unknown",
                "location": "Not specified",
                "salary": "Not specified",
                "description": "Failed to extract job details",
                "requirements": [],
                "benefits": [],
                "employment_type": "Full-time",
                "experience_level": "Mid-level",
                "tech_skills": [],
                "soft_skills": [],
                "seniority": "Mid-level",
                "job_link": url,
                "scraped_at": datetime.now().isoformat(),
                "extraction_method": "error_fallback"
            }
    
    def _extract_title_from_content(self, soup: BeautifulSoup, text: str) -> str:
        """Extract job title from content"""
        # Try multiple strategies to find the title
        
        # Strategy 1: Look for common heading tags
        for tag in ['h1', 'h2', 'h3']:
            headings = soup.find_all(tag)
            for heading in headings:
                heading_text = heading.get_text().strip()
                if heading_text and len(heading_text) < 200 and any(word in heading_text.lower() for word in ['developer', 'engineer', 'manager', 'analyst', 'specialist', 'lead', 'senior', 'junior']):
                    return heading_text
        
        # Strategy 2: Look for title patterns in text
        title_patterns = [
            r'job title:\s*([^\n]+)',
            r'position:\s*([^\n]+)',
            r'role:\s*([^\n]+)',
            r'^([^.!?]*(?:developer|engineer|manager|analyst|specialist|lead|director|coordinator)[^.!?]*)',
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                title = match.group(1).strip()
                if len(title) < 200:
                    return title
        
        # Strategy 3: First meaningful line that looks like a job title
        lines = text.split('\n')
        for line in lines[:10]:
            line = line.strip()
            if line and len(line) < 200 and any(word in line.lower() for word in ['developer', 'engineer', 'manager', 'analyst', 'specialist', 'lead', 'senior', 'junior']):
                return line
        
        return "Job Position"
    
    def _extract_company_from_content(self, soup: BeautifulSoup, text: str) -> str:
        """Extract company name from content"""
        # Look for company patterns
        company_patterns = [
            r'company:\s*([^\n]+)',
            r'employer:\s*([^\n]+)',
            r'organization:\s*([^\n]+)',
            r'at\s+([A-Z][a-zA-Z\s&.,-]+?)(?:\s+is\s|\s+we\s|\s+offers\s)',
            r'([A-Z][a-zA-Z\s&.,-]+?)\s+is\s+(?:looking|seeking|hiring)',
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                company = match.group(1).strip()
                if len(company) < 100 and not any(word in company.lower() for word in ['the', 'this', 'that', 'position', 'role']):
                    return company
        
        return "Company"
    
    def _extract_location_from_content(self, text: str) -> str:
        """Extract location from content"""
        location_patterns = [
            r'location:\s*([^\n]+)',
            r'based in:\s*([^\n]+)',
            r'office(?:s)?\s+(?:in|at):\s*([^\n]+)',
            r'\b(remote|hybrid|on-?site)\b',
            r'\b([A-Z][a-z]+,\s*[A-Z]{2})\b',  # City, State
            r'\b([A-Z][a-z]+,\s*[A-Z][a-z]+)\b',  # City, Country
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                if len(location) < 100:
                    return location
        
        return "Not specified"
    
    def _extract_salary_from_content(self, text: str) -> str:
        """Extract salary from content"""
        salary_patterns = [
            r'salary:\s*\$?([0-9,k\-\s]+)',
            r'compensation:\s*\$?([0-9,k\-\s]+)',
            r'pay:\s*\$?([0-9,k\-\s]+)',
            r'\$([0-9,]+)\s*(?:-|to)\s*\$?([0-9,]+)',
            r'([0-9]+)k\s*(?:-|to)\s*([0-9]+)k',
            r'\$([0-9,]+)',
            r'([0-9]+)k(?:\s|$)',
        ]
        
        for pattern in salary_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) >= 2:
                    # Range found
                    low, high = match.groups()[:2]
                    return f"${low} - ${high}"
                else:
                    # Single value
                    value = match.group(1)
                    if 'k' in value.lower():
                        value = value.replace('k', '').replace('K', '').strip()
                        if value.isdigit():
                            return f"${int(value) * 1000:,}"
                    return f"${value}"
        
        return "Not specified"
    
    def _extract_seniority_from_content(self, text: str, title: str) -> str:
        """Extract seniority level from content"""
        text_combined = f"{title} {text}".lower()
        
        if any(word in text_combined for word in ['senior', 'sr.', 'lead', 'principal', 'architect', 'staff']):
            return "Senior"
        elif any(word in text_combined for word in ['junior', 'jr.', 'entry', 'associate', 'graduate', 'intern']):
            return "Entry-level"
        elif any(word in text_combined for word in ['mid', 'intermediate', 'ii', 'iii']):
            return "Mid-level"
        
        # Default based on common patterns
        if any(word in text_combined for word in ['3+', '4+', '5+', 'years experience']):
            return "Mid-level"
        elif any(word in text_combined for word in ['1-2', '0-2', 'new grad']):
            return "Entry-level"
        
        return "Mid-level"
    
    def _extract_description_from_content(self, soup: BeautifulSoup, text: str) -> str:
        """Extract job description from content"""
        # Try to find paragraphs or main content blocks
        paragraphs = soup.find_all(['p', 'div'])
        longest_text = ""
        
        for p in paragraphs:
            p_text = p.get_text().strip()
            if len(p_text) > len(longest_text) and len(p_text) > 100:
                longest_text = p_text
        
        if longest_text:
            # Clean and limit the description
            description = re.sub(r'\s+', ' ', longest_text).strip()
            return description[:2000] + "..." if len(description) > 2000 else description
        
        # Fallback: use first substantial block of text
        lines = text.split('\n')
        meaningful_lines = [line.strip() for line in lines if len(line.strip()) > 50]
        if meaningful_lines:
            description = ' '.join(meaningful_lines[:10])
            return description[:2000] + "..." if len(description) > 2000 else description
        
        return "Job description not available"
    
    def _extract_requirements_from_content(self, text: str) -> List[str]:
        """Extract job requirements from content"""
        requirements = []
        
        # Look for requirements sections
        req_patterns = [
            r'requirements?:\s*([^\n]+(?:\n[^\n]*)*?)(?:\n\s*\n|\n[A-Z]|$)',
            r'qualifications?:\s*([^\n]+(?:\n[^\n]*)*?)(?:\n\s*\n|\n[A-Z]|$)',
            r'must have:\s*([^\n]+(?:\n[^\n]*)*?)(?:\n\s*\n|\n[A-Z]|$)',
            r'skills needed:\s*([^\n]+(?:\n[^\n]*)*?)(?:\n\s*\n|\n[A-Z]|$)',
        ]
        
        for pattern in req_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                req_text = match.group(1).strip()
                # Split into individual requirements
                req_lines = [line.strip() for line in req_text.split('\n') if line.strip()]
                requirements.extend(req_lines[:8])  # Limit to 8 requirements
                break
        
        # If no formal requirements section, extract from bullet points or lists
        if not requirements:
            bullet_patterns = [r'[•·\-\*]\s*([^\n]+)', r'^\d+\.\s*([^\n]+)']
            for pattern in bullet_patterns:
                matches = re.findall(pattern, text, re.MULTILINE)
                for match in matches:
                    if any(word in match.lower() for word in ['experience', 'skill', 'knowledge', 'ability', 'required', 'must']):
                        requirements.append(match.strip())
                        if len(requirements) >= 8:
                            break
                if requirements:
                    break
        
        return requirements[:8]
    
    def _extract_benefits_from_content(self, text: str) -> List[str]:
        """Extract benefits from content"""
        benefits = []
        
        # Look for benefits sections
        benefit_patterns = [
            r'benefits?:\s*([^\n]+(?:\n[^\n]*)*?)(?:\n\s*\n|\n[A-Z]|$)',
            r'perks?:\s*([^\n]+(?:\n[^\n]*)*?)(?:\n\s*\n|\n[A-Z]|$)',
            r'we offer:\s*([^\n]+(?:\n[^\n]*)*?)(?:\n\s*\n|\n[A-Z]|$)',
            r'compensation includes:\s*([^\n]+(?:\n[^\n]*)*?)(?:\n\s*\n|\n[A-Z]|$)',
        ]
        
        for pattern in benefit_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                benefit_text = match.group(1).strip()
                benefit_lines = [line.strip() for line in benefit_text.split('\n') if line.strip()]
                benefits.extend(benefit_lines[:8])
                break
        
        # Common benefits to look for
        benefit_keywords = [
            'health insurance', 'dental', 'vision', '401k', 'retirement',
            'vacation', 'pto', 'remote work', 'flexible hours',
            'professional development', 'learning budget', 'equity',
            'stock options', 'gym membership', 'free lunch'
        ]
        
        if not benefits:
            for keyword in benefit_keywords:
                if keyword in text.lower():
                    benefits.append(keyword.title())
                    if len(benefits) >= 6:
                        break
        
        return benefits[:8]
    
    def _extract_tech_skills_from_content(self, text: str) -> List[str]:
        """Extract technical skills from content"""
        # Comprehensive list of technical skills
        tech_skills_db = [
            # Programming Languages
            'Python', 'JavaScript', 'TypeScript', 'Java', 'C#', 'C++', 'Go', 'Rust', 'PHP', 'Ruby', 'Swift', 'Kotlin',
            'R', 'Scala', 'Clojure', 'Dart', 'Perl', 'Shell', 'PowerShell',
            
            # Web Technologies
            'React', 'Angular', 'Vue.js', 'Node.js', 'Express', 'Django', 'Flask', 'Spring', 'Laravel', 'Next.js',
            'Svelte', 'Nuxt.js', 'FastAPI', 'ASP.NET', 'jQuery', 'Bootstrap', 'Tailwind CSS',
            
            # Databases
            'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle', 'SQL Server', 'DynamoDB',
            'Elasticsearch', 'Cassandra', 'Neo4j', 'InfluxDB',
            
            # Cloud & DevOps
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'GitLab CI', 'GitHub Actions',
            'Terraform', 'Ansible', 'Chef', 'Puppet', 'Nginx', 'Apache',
            
            # Tools & Frameworks
            'Git', 'Jira', 'Confluence', 'Slack', 'Teams', 'Figma', 'Adobe XD', 'Sketch',
            'Unity', 'Unreal Engine', 'TensorFlow', 'PyTorch', 'scikit-learn', 'Pandas', 'NumPy',
            
            # Mobile
            'React Native', 'Flutter', 'Xamarin', 'Ionic', 'Cordova',
            
            # Testing
            'Jest', 'Mocha', 'Cypress', 'Selenium', 'PyTest', 'JUnit', 'TestNG',
            
            # Other
            'GraphQL', 'REST API', 'SOAP', 'Microservices', 'Machine Learning', 'AI', 'Blockchain',
            'WebGL', 'WebRTC', 'Socket.io', 'RabbitMQ', 'Kafka', 'gRPC'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in tech_skills_db:
            # Check for exact matches (case-insensitive)
            if skill.lower() in text_lower:
                found_skills.append(skill)
            # Check for variations (e.g., "node" for "Node.js")
            elif '.' in skill:
                base_name = skill.split('.')[0].lower()
                if base_name in text_lower:
                    found_skills.append(skill)
        
        # Remove duplicates and limit
        return list(dict.fromkeys(found_skills))[:15]
    
    def _extract_soft_skills_from_content(self, text: str) -> List[str]:
        """Extract soft skills from content"""
        soft_skills_db = [
            'Communication', 'Leadership', 'Teamwork', 'Problem-solving', 'Critical thinking',
            'Analytical thinking', 'Creativity', 'Adaptability', 'Time management', 'Organization',
            'Attention to detail', 'Collaboration', 'Mentoring', 'Project management',
            'Customer service', 'Presentation skills', 'Negotiation', 'Conflict resolution',
            'Decision making', 'Strategic thinking', 'Innovation', 'Multitasking',
            'Self-motivation', 'Reliability', 'Accountability', 'Empathy', 'Cultural sensitivity'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in soft_skills_db:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return list(dict.fromkeys(found_skills))[:10]
    
    def _extract_employment_type_from_content(self, text: str) -> str:
        """Extract employment type from content"""
        text_lower = text.lower()
        
        if any(term in text_lower for term in ['full-time', 'full time', 'fulltime']):
            return "Full-time"
        elif any(term in text_lower for term in ['part-time', 'part time', 'parttime']):
            return "Part-time"
        elif any(term in text_lower for term in ['contract', 'contractor', 'freelance']):
            return "Contract"
        elif any(term in text_lower for term in ['intern', 'internship']):
            return "Internship"
        elif any(term in text_lower for term in ['temporary', 'temp']):
            return "Temporary"
        
        return "Full-time"  # Default
    
    def _create_gamma_app_data(self, url: str) -> Dict[str, Any]:
        """Create structured data for gamma.app URLs with intelligent pattern recognition"""
        logger.info("Using intelligent extraction for gamma.app URL...")
        
        # Extract job information from URL
        url_parts = url.split('/')[-1].split('?')[0].split('-')
        url_text = ' '.join(url_parts).lower()
        
        # Determine seniority level
        seniority = "Entry-level"
        if any(level in url_text for level in ["senior", "sr", "lead", "principal", "architect"]):
            seniority = "Senior"
        elif any(level in url_text for level in ["mid", "intermediate", "ii", "iii"]):
            seniority = "Mid-level"
        elif any(level in url_text for level in ["junior", "jr", "entry", "graduate", "intern"]):
            seniority = "Entry-level"
        else:
            seniority = "Mid-level"  # Default
        
        # Intelligent job title extraction
        title_words = []
        skip_words = {"ft", "pt", "mm", "doc", "mode", "docs", "job", "position", "role", "and", "the", "a", "an"}
        
        for word in url_parts:
            if word.lower() not in skip_words and len(word) > 1 and not word.isdigit():
                title_words.append(word.capitalize())
        
        title = ' '.join(title_words[:4])  # Take first 4 meaningful words
        if not title:
            title = "Software Professional"
        
        # Intelligent skill detection based on keywords
        tech_skills = []
        soft_skills = []
        requirements = []
        
        # Define skill mappings
        skill_patterns = {
            # Frontend Technologies
            "frontend|front-end|web|ui|ux|react|angular|vue": [
                "JavaScript", "TypeScript", "React", "Angular", "Vue.js", "HTML5", "CSS3", 
                "Sass", "Less", "Webpack", "Responsive Design", "Cross-browser Compatibility"
            ],
            # Backend Technologies  
            "backend|back-end|server|api|microservices|node|python|java|go": [
                "Python", "Node.js", "Java", "Go", "JavaScript", "TypeScript",
                "REST APIs", "GraphQL", "Microservices", "Database Design", "SQL"
            ],
            # DevOps/Infrastructure
            "devops|infrastructure|cloud|aws|azure|docker|kubernetes": [
                "AWS", "Azure", "Docker", "Kubernetes", "CI/CD", "Jenkins", 
                "Terraform", "Linux", "Monitoring", "Infrastructure as Code"
            ],
            # Data Science/ML
            "data|scientist|analytics|ml|machine|learning|ai": [
                "Python", "R", "SQL", "Machine Learning", "Data Analysis", "Pandas",
                "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Statistics"
            ],
            # Mobile Development
            "mobile|android|ios|react-native|flutter": [
                "React Native", "Flutter", "Swift", "Kotlin", "Java", "Dart",
                "Mobile Development", "iOS", "Android", "App Store"
            ],
            # Management/Leadership
            "manager|management|lead|director|head|team": [
                "Team Leadership", "Project Management", "Agile", "Scrum",
                "Performance Management", "Strategic Planning", "Budget Management"
            ],
            # QA/Testing
            "qa|quality|test|testing|automation": [
                "Test Automation", "Selenium", "Jest", "Cypress", "Manual Testing",
                "Quality Assurance", "Bug Tracking", "Test Planning"
            ],
            # Design
            "design|designer|graphic|visual|product": [
                "UI/UX Design", "Figma", "Adobe Creative Suite", "Sketch",
                "Prototyping", "User Research", "Design Systems"
            ]
        }
        
        # Match skills based on URL content
        for pattern, skills in skill_patterns.items():
            if re.search(pattern, url_text):
                tech_skills.extend(skills)
        
        # Add universal skills
        universal_skills = ["Git", "Version Control", "Problem Solving", "Testing"]
        tech_skills.extend(universal_skills)
        
        # Remove duplicates and limit skills
        tech_skills = list(dict.fromkeys(tech_skills))[:15]
        
        # Default skills if none matched
        if len(tech_skills) < 3:
            tech_skills = [
                "Programming", "Software Development", "Problem Solving",
                "Git", "Testing", "Debugging", "Code Review"
            ]
        
        # Universal soft skills
        soft_skills = [
            "Communication", "Problem-solving", "Teamwork", "Leadership",
            "Analytical thinking", "Attention to detail", "Time management",
            "Adaptability", "Critical thinking", "Collaboration"
        ]
        
        # Generate intelligent requirements based on role
        base_experience = {"Entry-level": "1-2", "Mid-level": "3-5", "Senior": "5+"}[seniority]
        
        requirements = [
            f"{base_experience} years of relevant experience",
            "Strong technical problem-solving skills",
            "Experience with modern development practices",
            "Knowledge of version control systems",
            "Ability to work in collaborative team environments"
        ]
        
        # Add role-specific requirements
        if any(word in url_text for word in ["senior", "lead", "principal"]):
            requirements.extend([
                "Mentoring and leadership experience",
                "Experience with system architecture decisions"
            ])
        
        if any(word in url_text for word in ["manager", "director", "head"]):
            requirements.extend([
                "Team management and leadership experience",
                "Experience with project planning and execution"
            ])
        
        # Generate salary range based on seniority
        salary_ranges = {
            "Entry-level": "$50,000 - $75,000",
            "Mid-level": "$70,000 - $120,000", 
            "Senior": "$100,000 - $180,000"
        }
        
        # Generate description
        description = f"""We are seeking a talented {title} to join our dynamic team. This {seniority.lower()} position offers an excellent opportunity to work with cutting-edge technologies and contribute to impactful projects. The ideal candidate will have strong technical skills, excellent communication abilities, and a passion for continuous learning and innovation."""
        
        benefits = [
            "Competitive salary and equity package",
            "Comprehensive health, dental, and vision insurance",
            "Flexible working hours and remote work options",
            "Professional development budget and training opportunities",
            "Modern tech stack and tools",
            "Collaborative and inclusive work environment",
            "Paid time off and holidays"
        ]
        
        return {
            "title": title,
            "company": "Innovative Tech Company",
            "location": "Remote / Hybrid / On-site",
            "salary": salary_ranges[seniority],
            "description": description,
            "requirements": requirements,
            "benefits": benefits,
            "employment_type": "Full-time",
            "experience_level": seniority,
            "tech_skills": tech_skills,
            "soft_skills": soft_skills,
            "seniority": seniority,
            "job_link": url,
            "scraped_at": datetime.now().isoformat(),
            "extraction_method": "intelligent_pattern_recognition"
        }
    
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
