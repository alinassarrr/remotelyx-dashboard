#!/usr/bin/env python3
"""
Example usage of the AI-powered job scraper
"""

import os
from gamma_job_scraper import GammaJobScraper

def main():
    # NO API KEY NEEDED! 100% FREE with Ollama
    print("🆓 This scraper is completely FREE - no API keys required!")
    print("🤖 Using Ollama (local AI) - Llama 3.2 model")
    
    # Example job URLs to test
    job_urls = [
        "https://gamma.app/docs/Full-Stack-Developer-IC-3s64m1oqf3nuf5u?mode=doc",
        # Add more URLs here to test
    ]
    
    print("🚀 FREE AI-Powered Job Scraper Demo")
    print("="*60)
    
    for url in job_urls:
        print(f"\n📋 Scraping: {url}")
        print("-" * 60)
        
        with GammaJobScraper() as scraper:
            # Use AI extraction (default)
            job_data = scraper.scrape_job(url, use_ai=True)
            
            if job_data:
                print("✅ Success! Extracted job data:")
                print(f"  📝 Title: {job_data.get('title', 'N/A')}")
                print(f"  🏢 Company: {job_data.get('company', 'N/A')}")
                print(f"  📍 Location: {job_data.get('location', 'N/A')}")
                print(f"  💼 Type: {job_data.get('employment_type', 'N/A')}")
                print(f"  💰 Salary: {job_data.get('salary', 'N/A')}")
                print(f"  📊 Seniority: {job_data.get('seniority', 'N/A')}")
                print(f"  🛠️  Tech Skills: {', '.join(job_data.get('tech_skills', []))}")
                print(f"  🤝 Soft Skills: {', '.join(job_data.get('soft_skills', []))}")
                print(f"  📄 Description: {job_data.get('description', 'N/A')[:100]}...")
            else:
                print("❌ Failed to extract job data")

if __name__ == "__main__":
    main()
