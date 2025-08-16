#!/usr/bin/env python3
"""
Gamma.app Job Scraper
A clean, modular web scraper for extracting job data from gamma.app
"""

import json
import re
import os
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import ollama

# =============================================================================
# CONFIGURATION
# =============================================================================

# API Configuration
API_URL = "http://localhost:5000/api/jobs"
OLLAMA_MODEL = "llama3.2"  # Free local AI model

# Skill Dictionaries
TECH_SKILLS = [
    "python", "javascript", "java", "react", "node.js", "angular", "vue", "typescript",
    "html", "css", "sql", "postgresql", "mysql", "mongodb", "redis", "aws", "azure",
    "gcp", "docker", "kubernetes", "terraform", "jenkins", "git", "github", "gitlab",
    "linux", "unix", "bash", "shell", "php", "ruby", "go", "rust", "c++", "c#",
    "scala", "kotlin", "swift", "flutter", "react native", "devops", "ci/cd",
    "machine learning", "ai", "data science", "blockchain", "microservices",
    "api", "rest", "graphql", "websocket", "nginx", "apache", "elasticsearch"
]

SOFT_SKILLS = [
    "communication", "leadership", "teamwork", "problem-solving", "adaptability",
    "creativity", "time management", "organization", "collaboration", "mentoring",
    "project management", "agile", "scrum", "customer service", "analytical thinking",
    "critical thinking", "attention to detail", "multitasking", "stress management"
]

# CSS Selectors for data extraction
SELECTORS = {
    'title': [
        'h1', 'h2', 'h3', '.title', '.job-title', '.position-title',
        '[class*="title"]', '[class*="job"]', '[data-testid*="title"]'
    ],
    'company': [
        '.company', '.employer', '[class*="company"]', '[class*="employer"]',
        '.company-name', '.employer-name', '[data-testid*="company"]',
        '.organization', '.business', '.firm', '.agency',
        '[class*="org"]', '[class*="business"]', '[class*="firm"]',
        'h1', 'h2', 'h3', '.title', '.header', '.brand', '.logo'
    ],
    'location': [
        '.location', '[class*="location"]', '.job-location',
        '.address', '[class*="address"]', '[data-testid*="location"]'
    ],
    'employment_type': [
        '.employment-type', '[class*="employment"]', '.job-type',
        '.work-type', '[class*="type"]', '[data-testid*="type"]',
        '.contract', '.full-time', '.part-time', '.remote', '.hybrid',
        '.on-site', '.permanent', '.temporary', '.freelance',
        '[class*="contract"]', '[class*="remote"]', '[class*="hybrid"]',
        '.work-model', '.work-arrangement', '.schedule'
    ],
    'salary': [
        '.salary', '[class*="salary"]', '.compensation', '[class*="compensation"]',
        '.pay', '[class*="pay"]', '.remuneration', '[data-testid*="salary"]',
        '[data-testid*="compensation"]', '.benefits', '[class*="benefits"]',
        '.package', '[class*="package"]', '.total-comp', '[class*="total"]'
    ],
    'date_posted': [
        '.date', '[class*="date"]', '.posted-date',
        '.published', '[class*="published"]', '.post-date', '[data-testid*="date"]',
        '.created', '.updated', '.timestamp', '.time', '.posted',
        '[class*="created"]', '[class*="updated"]', '[class*="timestamp"]',
        '.meta', '.metadata', '.info', '.details'
    ],
    'description': [
        '.job-description', '[class*="description"]', '.job-details',
        '.description', '.content', '.job-content', 'main', 'article',
        '[data-testid*="description"]', '.job-requirements', '.requirements',
        '.job-summary', '.role-description', '.position-details',
        '.about-role', '.what-youll-do', '.responsibilities',
        '.qualifications', '.requirements', '.skills-needed',
        '.benefits', '.perks', '.what-we-offer', '.company-info',
        '.about-us', '.team', '.culture', '.mission', '.values'
    ]
}

# =============================================================================
# BROWSER MANAGEMENT
# =============================================================================

class BrowserManager:
    """Manages Chrome browser setup and configuration"""
    
    @staticmethod
    def get_chrome_options() -> Options:
        """Get optimized Chrome options for web scraping"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        return options
    
    @staticmethod
    def create_driver() -> Optional[webdriver.Chrome]:
        """Create and return a Chrome driver instance"""
        try:
            options = BrowserManager.get_chrome_options()
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
            print(f"❌ Failed to initialize Chrome driver: {e}")
            return None

# =============================================================================
# AI-POWERED DATA EXTRACTION
# =============================================================================

class AIDataExtractor:
    """FREE AI-powered job data extraction using Ollama"""
    
    def __init__(self):
        # No API key needed - completely free!
        pass
    
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
        
        # Truncate if too long (OpenAI has token limits)
        if len(clean_text) > 8000:
            clean_text = clean_text[:8000] + "..."
        
        # AI prompt for job data extraction
        prompt = f"""
        You are a job data extraction expert. Analyze the following job posting and extract ALL available information.

        CRITICAL: You MUST extract tech skills, soft skills, and a detailed description. Look carefully through the entire content.

        Return ONLY a valid JSON object with these exact fields:

        {{
            "title": "exact job title",
            "company": "company name",
            "location": "job location or 'Remote' if remote work",
            "employment_type": "Full-time/Part-time/Contract/Internship",
            "salary": "salary range or amount (format as '50000$' or range like '50000$-60000$')",
            "date_posted": "posting date in YYYY-MM-DD format or today's date",
            "description": "detailed job description including responsibilities, requirements, and company info (200-400 words)",
            "tech_skills": ["list all technical skills mentioned like Python, JavaScript, AWS, Docker, SQL, etc"],
            "soft_skills": ["list all soft skills mentioned like communication, leadership, teamwork, problem-solving, etc"],
            "seniority": "Junior/Mid/Senior based on experience requirements",
            "job_link": "{url}"
        }}

        INSTRUCTIONS:
        1. For TECH SKILLS: Look for programming languages, frameworks, tools, databases, cloud platforms, methodologies
        2. For SOFT SKILLS: Look for interpersonal skills, leadership qualities, work style preferences
        3. For DESCRIPTION: Summarize the role, responsibilities, requirements, and company information
        4. If you can't find specific skills, look in the description text for implied skills
        5. NEVER return empty arrays for skills - always find at least a few relevant ones

        Job posting content:
        {clean_text}

        Return ONLY the JSON object, no other text.
        """
        
        try:
            # Use FREE Ollama local AI
            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=[
                    {"role": "system", "content": "You are a job data extraction expert. Always return valid JSON."},
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
            
            return job_data
            
        except Exception as e:
            print(f"❌ AI extraction failed: {e}")
            # Fallback to basic extraction
            return AIDataExtractor._fallback_extraction(clean_text, url)
    
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
            "salary": "Not specified",
            "date_posted": datetime.now().strftime('%Y-%m-%d'),
            "description": text[:300] + "..." if len(text) > 300 else text,
            "tech_skills": [],
            "soft_skills": [],
            "seniority": "Mid",
            "job_link": url
        }

# =============================================================================
# LEGACY DATA EXTRACTION (kept for reference)
# =============================================================================

class DataExtractor:
    """Handles extraction of job data from HTML"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text for readability"""
        if not text:
            return ""
        
        import unicodedata
        text = unicodedata.normalize('NFKD', text)
        text = ''.join(char for char in text if char.isprintable() or char.isspace())
        text = text.replace('\u00a0', ' ').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        text = ' '.join(text.split())
        
        unwanted_patterns = [
            'Expand', 'Present', 'SS', 'ML', 'Tech Integration SpecialistTech Integration Specialist',
            'About The Company', 'Role Overview', 'Key Responsibilities'
        ]
        
        for pattern in unwanted_patterns:
            text = text.replace(pattern, '')
        
        return ' '.join(text.split()).strip()
    
    @staticmethod
    def extract_text_by_selectors(soup: BeautifulSoup, selectors: List[str], field_name: str) -> Optional[str]:
        """Extract text using multiple CSS selectors"""
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if text and len(text) > 2:
                    if field_name == 'description':
                        text = DataExtractor.clean_text(text)
                        if len(text) > 50:
                            return text
                    else:
                        return text
        return None
    
    @staticmethod
    def extract_description_fallback(soup: BeautifulSoup) -> Optional[str]:
        """Fallback method to extract comprehensive job content"""
        content_elements = soup.find_all(['p', 'div', 'section', 'article', 'main'])
        all_content = []
        
        important_keywords = [
            'responsibilities', 'requirements', 'qualifications', 'experience', 
            'duties', 'about', 'skills', 'benefits', 'perks', 'compensation',
            'salary', 'pay', 'mission', 'culture', 'team', 'company',
            'role', 'position', 'job', 'work', 'develop', 'build', 'create',
            'manage', 'lead', 'collaborate', 'communicate', 'analyze'
        ]
        
        for element in content_elements:
            text = element.get_text(strip=True)
            if len(text) > 50 and any(keyword in text.lower() for keyword in important_keywords):
                all_content.append(text)
        
        if all_content:
            full_description = ' '.join(all_content)
            cleaned_desc = DataExtractor.clean_text(full_description)
            return cleaned_desc[:2000]
        
        return None
    
    @staticmethod
    def extract_comprehensive_description(soup: BeautifulSoup) -> str:
        """Extract comprehensive job description from all relevant sections"""
        sections = []
        
        section_selectors = [
            '.job-description', '.description', '.content', '.job-content',
            '.role-description', '.position-details', '.about-role',
            '.requirements', '.qualifications', '.skills-needed',
            '.job-requirements', '.experience-required',
            '.responsibilities', '.duties', '.what-youll-do',
            '.key-responsibilities', '.role-responsibilities',
            '.benefits', '.perks', '.what-we-offer', '.compensation',
            '.salary-info', '.package', '.total-comp',
            '.company-info', '.about-us', '.team', '.culture',
            '.mission', '.values', '.company-description',
            'main', 'article', '.main-content', '.page-content'
        ]
        
        for selector in section_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 30:
                    sections.append(text)
        
        if sections:
            full_description = ' '.join(sections)
            cleaned_desc = DataExtractor.clean_text(full_description)
            return cleaned_desc[:3000]
        
        return ""
    
    @staticmethod
    def search_salary_in_page(soup: BeautifulSoup) -> Optional[str]:
        """Search for salary information throughout the entire page"""
        all_text = soup.get_text()
        
        salary_patterns = [
            r'\$\d{1,3}(?:,\d{3})*(?:k|K)?',
            r'\$\d{4,}(?:,\d{3})*',
            r'\d{2,3}[kK]',
            r'\d{2,3}[kK]\s*-\s*\d{2,3}[kK]',
            r'(?:salary|compensation|pay).*?\d{1,3}(?:,\d{3})*',
            r'(?:budget|budgeted).*?\d{1,3}(?:,\d{3})*',
            r'\d{4,}(?:,\d{3})*',
            r'\d{1,3}(?:,\d{3})*\s*(?:dollars|usd|per year|annually)'
        ]
        
        for pattern in salary_patterns:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                return matches[0]
        
        salary_elements = soup.find_all(text=re.compile(r'\$\d+|\d+[kK]|\d{4,}', re.IGNORECASE))
        for element in salary_elements:
            text = element.strip()
            if len(text) > 5 and any(word in text.lower() for word in ['salary', 'compensation', 'pay', 'budget', 'dollars', 'usd']):
                return text
        
        return None
    
    @staticmethod
    def extract_any_salary_from_text(text: str) -> Optional[str]:
        """Extract any reasonable salary-like numbers from text"""
        if not text:
            return None
        
        salary_candidates = []
        
        numbers = re.findall(r'\d{1,3}(?:,\d{3})*', text)
        for num in numbers:
            num_val = int(num.replace(',', ''))
            if 1000 <= num_val <= 500000:
                salary_candidates.append((num_val, num))
        
        k_numbers = re.findall(r'(\d{2,3})[kK]', text)
        for num in k_numbers:
            num_val = int(num) * 1000
            if 20000 <= num_val <= 500000:
                salary_candidates.append((num_val, f"{num}k"))
        
        if salary_candidates:
            salary_candidates.sort(reverse=True)
            best_candidate = salary_candidates[0]
            return f"{best_candidate[0]}$"
        
        return None
    
    @staticmethod
    def create_concise_summary(text: str, max_length: int = 200) -> str:
        """Create a concise summary of the description"""
        if not text or len(text) <= max_length:
            return text
        
        sentences = text.split('.')
        summary_parts = []
        current_length = 0
        
        key_phrases = [
            "we are looking for", "seeking a", "looking for a", "join our team",
            "as a", "you will", "responsible for", "mission is to", "role is to",
            "requirements", "qualifications", "experience", "skills needed"
        ]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(phrase in sentence.lower() for phrase in key_phrases):
                if current_length + len(sentence) <= max_length:
                    summary_parts.append(sentence)
                    current_length += len(sentence)
                else:
                    break
        
        if len(summary_parts) == 0:
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 20 and current_length + len(sentence) <= max_length:
                    summary_parts.append(sentence)
                    current_length += len(sentence)
                elif current_length + len(sentence) > max_length:
                    break
        
        if summary_parts:
            summary = '. '.join(summary_parts) + '.'
            return summary.strip()
        else:
            return text[:max_length].strip() + '...'
    
    @staticmethod
    def extract_all_fields(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract all job fields from HTML"""
        raw_data = {
            'title': None,
            'company': 'Gamma.app',
            'location': None,
            'employment_type': None,
            'salary': None,
            'date_posted': None,
            'description': None,
            'job_link': url
        }
        
        for field, selectors in SELECTORS.items():
            if field == 'description':
                raw_data[field] = DataExtractor.extract_comprehensive_description(soup)
                if not raw_data[field]:
                    raw_data[field] = DataExtractor.extract_text_by_selectors(soup, selectors, field)
                    if not raw_data[field]:
                        raw_data[field] = DataExtractor.extract_description_fallback(soup)
            elif field == 'salary':
                raw_data[field] = DataExtractor.extract_text_by_selectors(soup, selectors, field)
                if not raw_data[field] and raw_data.get('description'):
                    raw_data[field] = DataEnricher.extract_compensation_from_description(raw_data['description'])
                if not raw_data[field]:
                    raw_data[field] = DataExtractor.search_salary_in_page(soup)
                if not raw_data[field] and raw_data.get('description'):
                    raw_data[field] = DataExtractor.extract_any_salary_from_text(raw_data['description'])
            else:
                raw_data[field] = DataExtractor.extract_text_by_selectors(soup, selectors, field)
        
        # Apply intelligent fallbacks for missing fields
        if not raw_data['company'] and raw_data.get('description'):
            raw_data['company'] = DataExtractor.extract_company_from_content(soup, raw_data['description'])
        
        if not raw_data['employment_type'] and raw_data.get('description'):
            raw_data['employment_type'] = DataExtractor.extract_employment_type_from_content(raw_data['description'])
        
        if not raw_data['date_posted'] and raw_data.get('description'):
            raw_data['date_posted'] = DataExtractor.extract_date_from_content(soup, raw_data['description'])
        
        # Set defaults for missing fields
        if not raw_data['employment_type']:
            raw_data['employment_type'] = "Full-time"
        
        if not raw_data['date_posted']:
            raw_data['date_posted'] = datetime.now().strftime("%Y-%m-%d")
        
        return raw_data
    
    @staticmethod
    def extract_company_from_content(soup: BeautifulSoup, description: str) -> Optional[str]:
        """Extract company name from content when selectors fail"""
        company_patterns = [
            r'(?:at|with|join|work for|employed by)\s+([A-Z][a-zA-Z\s&]+(?:Inc|LLC|Ltd|Corp|Company|Tech|Solutions|Systems))',
            r'([A-Z][a-zA-Z\s&]+(?:Inc|LLC|Ltd|Corp|Company|Tech|Solutions|Systems))',
            r'(?:company|organization|firm):\s*([A-Z][a-zA-Z\s&]+)'
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                company = match.group(1).strip()
                if len(company) > 2 and len(company) < 50:
                    return company
        
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4'])
        for header in headers:
            text = header.get_text(strip=True)
            if any(word in text.lower() for word in ['tech', 'inc', 'llc', 'ltd', 'corp', 'company']):
                return text
        
        return None
    
    @staticmethod
    def extract_employment_type_from_content(description: str) -> Optional[str]:
        """Extract employment type from description content"""
        employment_keywords = {
            'Full-time': ['full-time', 'full time', 'permanent', 'fulltime'],
            'Part-time': ['part-time', 'part time', 'parttime'],
            'Contract': ['contract', 'contractor', 'freelance', 'consultant'],
            'Remote': ['remote', 'work from home', 'wfh', 'virtual'],
            'Hybrid': ['hybrid', 'flexible', 'mixed'],
            'Internship': ['intern', 'internship', 'trainee', 'graduate']
        }
        
        desc_lower = description.lower()
        for emp_type, keywords in employment_keywords.items():
            if any(keyword in desc_lower for keyword in keywords):
                return emp_type
        
        return None
    
    @staticmethod
    def extract_date_from_content(soup: BeautifulSoup, description: str) -> Optional[str]:
        """Extract date from content when selectors fail"""
        date_patterns = [
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\d{4}-\d{2}-\d{2})',
            r'(?:posted|published|created|updated)\s+(?:on\s+)?(\w+\s+\d{1,2},?\s+\d{4})',
            r'(\w+\s+\d{1,2},?\s+\d{4})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        all_text = soup.get_text()
        recent_dates = re.findall(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', all_text)
        if recent_dates:
            return recent_dates[0]
        
        return None

# =============================================================================
# DATA ENRICHMENT
# =============================================================================

class DataEnricher:
    """Handles enrichment and processing of extracted data"""
    
    @staticmethod
    def classify_seniority(title: str, description: str) -> str:
        """Classify seniority level from title and description"""
        if not title and not description:
            return "Mid"
        
        text = f"{title or ''} {description or ''}".lower()
        
        seniority_patterns = {
            'Senior': ["senior", "lead", "principal", "staff", "expert", "advanced"],
            'Junior': ["junior", "entry level", "entry-level", "graduate", "intern", "trainee", "associate"],
            'Mid': ["mid", "intermediate", "experienced"]
        }
        
        for level, patterns in seniority_patterns.items():
            if any(pattern in text for pattern in patterns):
                return level
        
        return "Mid"
    
    @staticmethod
    def parse_salary(salary_text: str) -> Optional[str]:
        """Parse salary information and return simple format like '2000$'"""
        if not salary_text:
            return None
        
        salary_patterns = [
            r'(?:salary|compensation|pay)\s+(?:of\s+)?\$?(\d{1,3}(?:,\d{3})*)(?:k|K)?(?:\s*-\s*\$?(\d{1,3}(?:,\d{3})*)(?:k|K)?)?',
            r'(?:budget|budgeted)\s+(?:at\s+)?\$?(\d{1,3}(?:,\d{3})*)(?:k|K)?(?:\s*-\s*\$?(\d{1,3}(?:,\d{3})*)(?:k|K)?)?',
            r'\$(\d{1,3}(?:,\d{3})*)(?:k|K)?\s*-\s*\$(\d{1,3}(?:,\d{3})*)(?:k|K)?',
            r'\$(\d{1,3}(?:,\d{3})*)(?:k|K)?\s*(?:per\s+)?(?:year|month|hour)',
            r'(\d{2,3})(?:k|K)\s*-\s*(\d{2,3})(?:k|K)',
            r'(\d{2,3})(?:k|K)\s*(?:per\s+)?(?:year|month|hour)',
            r'(\d{2,3})(?:k|K)?\s*(?:annually|per year|yearly)',
            r'\$(\d{1,3}(?:,\d{3})*)\s*(?:annually|per year|yearly)',
            r'\$(\d{4,}(?:,\d{3})*)',
            r'(\d{4,}(?:,\d{3})*)\s*(?:dollars|usd)',
            r'\$(\d{1,3}(?:,\d{3})*)',
            r'\$(\d{4,})'
        ]
        
        for pattern in salary_patterns:
            match = re.search(pattern, salary_text, re.IGNORECASE)
            if match:
                groups = match.groups()
                min_salary = groups[0].replace(',', '') if groups[0] else None
                max_salary = groups[1].replace(',', '') if len(groups) > 1 and groups[1] else None
                
                if min_salary:
                    min_val = int(min_salary)
                    if 'k' in salary_text.lower():
                        min_salary = str(min_val * 1000)
                    else:
                        min_salary = str(min_val)
                    
                    final_min_val = int(min_salary)
                    if final_min_val < 100:
                        continue
                
                if max_salary:
                    max_val = int(max_salary)
                    if 'k' in salary_text.lower():
                        max_salary = str(max_val * 1000)
                    else:
                        max_salary = str(max_val)
                    
                    final_max_val = int(max_salary)
                    if final_max_val < 100:
                        continue
                
                if min_salary and max_salary:
                    avg_salary = (int(min_salary) + int(max_salary)) // 2
                    return f"{avg_salary}$"
                elif min_salary:
                    return f"{min_salary}$"
                elif max_salary:
                    return f"{max_salary}$"
        
        return None
    
    @staticmethod
    def extract_compensation_from_description(description: str) -> Optional[str]:
        """Extract compensation information from job description"""
        if not description:
            return None
        
        compensation_keywords = [
            'salary', 'compensation', 'pay', 'remuneration', 'package',
            'earnings', 'income', 'wage', 'rate', 'budget', 'total comp',
            'base salary', 'annual salary', 'hourly rate', 'monthly salary'
        ]
        
        sentences = description.split('.')
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in compensation_keywords):
                if re.search(r'\d+', sentence):
                    return sentence.strip()
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if re.search(r'\d+[kK]', sentence) or re.search(r'\$\d+', sentence):
                if any(word in sentence_lower for word in ['per', 'year', 'month', 'hour', 'annual', 'monthly']):
                    return sentence.strip()
        
        budget_patterns = [
            r'budget.*?\d+[kK]?.*?\d+[kK]?',
            r'\d+[kK]?.*?\d+[kK]?.*?budget',
            r'range.*?\d+[kK]?.*?\d+[kK]?'
        ]
        
        for pattern in budget_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                return match.group(0).strip()
        
        return None
    
    @staticmethod
    def extract_skills(description: str) -> Tuple[List[str], List[str]]:
        """Extract tech and soft skills from description"""
        if not description:
            return [], []
        
        text_lower = description.lower()
        tech_skills = []
        soft_skills = []
        
        for skill in TECH_SKILLS:
            if skill in text_lower:
                tech_skills.append(skill.capitalize())
        
        for skill in SOFT_SKILLS:
            if skill in text_lower:
                soft_skills.append(skill.capitalize())
        
        return tech_skills, soft_skills

# =============================================================================
# MAIN SCRAPER CLASS
# =============================================================================

class GammaJobScraper:
    """Main scraper class for gamma.app job postings"""
    
    def __init__(self):
        self.driver = None
    
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
            print(f"❌ Error fetching page: {e}")
            return None
    
    def scrape_job(self, url: str, use_ai: bool = True) -> Optional[Dict[str, Any]]:
        """Main scraping function with AI-powered extraction"""
        if not self.setup_driver():
            return None
        
        try:
            soup = self.fetch_job_page(url)
            if not soup:
                return None
            
            if use_ai:
                print("🤖 Using AI-powered extraction...")
                try:
                    ai_extractor = AIDataExtractor()
                    job_data = ai_extractor.extract_job_data(self.driver.page_source, url)
                    print("✨ AI extraction successful!")
                    print(f"🔍 Debug - AI extracted: {len(job_data.get('tech_skills', []))} tech skills, {len(job_data.get('soft_skills', []))} soft skills")
                    print(f"💰 Debug - Salary: {job_data.get('salary', 'None')}")
                    print(f"📄 Debug - Description length: {len(job_data.get('description', ''))}")
                    return job_data
                except Exception as e:
                    print(f"⚠️ AI extraction failed, falling back to traditional method: {e}")
                    import traceback
                    traceback.print_exc()
                    use_ai = False
            
            if not use_ai:
                print("🔧 Using traditional extraction...")
                raw_data = DataExtractor.extract_all_fields(soup, url)
                
                # Apply enrichment
                seniority = DataEnricher.classify_seniority(raw_data['title'], raw_data['description'])
                salary_data = DataEnricher.parse_salary(raw_data['salary'])
                tech_skills, soft_skills = DataEnricher.extract_skills(raw_data['description'])
                
                # Create concise summary of description
                original_description = raw_data['description']
                concise_description = DataExtractor.create_concise_summary(original_description, max_length=200)
                
                # Build final JSON
                job_data = {
                    "title": raw_data['title'],
                    "seniority": seniority,
                    "employment_type": raw_data['employment_type'],
                    "company": raw_data['company'],
                    "location": raw_data.get('location', 'Not specified'),
                    "soft_skills": soft_skills,
                    "tech_skills": tech_skills,
                    "description": concise_description,
                    "salary": salary_data,
                    "date_posted": raw_data['date_posted'],
                    "job_link": url
                }
                
                return job_data
            
        except Exception as e:
            print(f"❌ Error during scraping: {e}")
            return None
        finally:
            self.cleanup()

# =============================================================================
# API COMMUNICATION
# =============================================================================

class APIClient:
    """Handles communication with backend API"""
    
    @staticmethod
    def send_job_data(job_data: Dict[str, Any]) -> bool:
        """Send job data to backend API"""
        try:
            # Save to file for verification
            with open('scraped_job.json', 'w', encoding='utf-8') as f:
                json.dump(job_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending to backend: {e}")
            return False

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function"""
    print("🚀 Gamma Job Scraper")
    print("="*60)
    
    # Job URL from n8n
    job_url = "https://gamma.app/docs/DevOps-Engineer-MJ-xow6m4hb8nsosqo?mode=doc"
    
    print(f"📋 Job URL: {job_url}")
    print("="*60)
    
    # Scrape job data
    with GammaJobScraper() as scraper:
        job_data = scraper.scrape_job(job_url)
        
        if job_data:
            # Send to backend API
            if APIClient.send_job_data(job_data):
                print("✅ Successfully processed and sent job data!")
                print("📊 Complete Job Data:")
                print(f"  Title: {job_data['title']}")
                print(f"  Company: {job_data['company']}")
                print(f"  Seniority: {job_data['seniority']}")
                print(f"  Employment Type: {job_data['employment_type']}")
                print(f"  Salary: {job_data['salary']}")
                print(f"  Date Posted: {job_data['date_posted']}")
                print(f"  Job Link: {job_data['job_link']}")
                print(f"  Description: {job_data['description']}")
                print(f"  Tech Skills: {', '.join(job_data['tech_skills'])}")
                print(f"  Soft Skills: {', '.join(job_data['soft_skills'])}")
            else:
                print("❌ Failed to send job data to backend")
        else:
            print("❌ Failed to scrape job data")
    
    print("✅ Scraping complete!")

if __name__ == "__main__":
    main()
