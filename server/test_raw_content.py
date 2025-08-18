#!/usr/bin/env python3
"""
Raw content extractor to see EXACTLY what's on the gamma.app page
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_raw_content(url):
    """Get raw content from gamma.app page"""
    print(f"Fetching: {url}")
    
    # Set up Chrome with realistic browser settings
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # Add realistic user agent and settings
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Enable JavaScript
    options.add_argument("--enable-javascript")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.set_page_load_timeout(60)
        
        # Hide automation detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        driver.get(url)
        
        print("Waiting 45 seconds for content to load...")
        time.sleep(45)
        
        # Try multiple interactions to trigger content loading
        try:
            # Scroll to trigger content
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(3)
            
            # Try clicking any buttons or interactive elements
            driver.execute_script("document.querySelectorAll('button, .btn, [role=button]').forEach(el => { try { el.click(); } catch(e) {} });")
            time.sleep(5)
            
            # Wait for any dynamic content
            driver.execute_script("setTimeout(() => {}, 5000);")
            time.sleep(5)
        except:
            pass
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Get all text
        text = soup.get_text(separator='\n', strip=True)
        
        print(f"\n{'='*50}")
        print("RAW PAGE CONTENT:")
        print(f"{'='*50}")
        print(text)
        print(f"{'='*50}")
        print(f"Total characters: {len(text)}")
        
        # Look for specific keywords
        keywords = ['compensation', 'salary', 'pay', '$', 'requirements', 'skills', 'experience']
        for keyword in keywords:
            if keyword.lower() in text.lower():
                print(f"✅ FOUND '{keyword}' in content")
            else:
                print(f"❌ NO '{keyword}' found")
        
        return text
        
    finally:
        driver.quit()

if __name__ == "__main__":
    url = "https://gamma.app/docs/Senior-Web-Developer-Department-Manager-MM-lfvkwq4cwjujukd?mode=doc"
    content = get_raw_content(url)
