"""
Configuration settings for the Job Scraper API
"""
import os

# API Configuration
API_HOST = '0.0.0.0'
API_PORT = int(os.getenv('PORT', 5000))
DEBUG_MODE = os.getenv('DEBUG', 'false').lower() == 'true'

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'job_scraper')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'jobs')

# AI Configuration
OLLAMA_MODEL = "llama3.2"

# Browser Configuration
BROWSER_OPTIONS = [
    '--headless',
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--window-size=1920,1080',
    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]
