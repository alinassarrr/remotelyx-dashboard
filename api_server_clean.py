"""
Clean Job Scraper API Server
REST API for n8n workflow integration with MongoDB storage
"""
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

from config import API_HOST, API_PORT, DEBUG_MODE
from database import DatabaseManager, CustomJSONEncoder
from scraper_core import JobScraper

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app setup
app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
CORS(app)

# Initialize database manager
db_manager = DatabaseManager()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    stats = db_manager.get_job_stats()
    return jsonify({
        "status": "healthy",
        "service": "Job Scraper API",
        "timestamp": datetime.now().isoformat(),
        "database_stats": stats
    })


@app.route('/scrape', methods=['POST'])
def scrape_job():
    """
    Main scraping endpoint for n8n workflow
    Expects: {"job_url": "https://..."}
    Returns: {"success": true, "data": {...}, "message": "..."}
    """
    try:
        # Validate request
        if not request.json or 'job_url' not in request.json:
            return jsonify({
                "success": False,
                "error": "Missing 'job_url' in request body",
                "example": {"job_url": "https://gamma.app/docs/..."}
            }), 400
        
        job_url = request.json['job_url'].strip()
        
        # Validate URL
        if not job_url or not job_url.startswith(('http://', 'https://')):
            return jsonify({
                "success": False,
                "error": "Invalid job URL provided",
                "provided_url": job_url
            }), 400
        
        logger.info(f"🚀 Starting scrape for: {job_url}")
        
        # Scrape the job
        with JobScraper() as scraper:
            job_data = scraper.scrape_job(job_url)
        
        if not job_data:
            return jsonify({
                "success": False,
                "error": "Failed to scrape job data",
                "job_url": job_url
            }), 500
        
        # Save to MongoDB
        save_success, save_message = db_manager.save_job(job_data)
        
        if not save_success:
            logger.warning(f"⚠️ Scraping successful but save failed: {save_message}")
            return jsonify({
                "success": True,
                "data": job_data,
                "warning": f"Job scraped but not saved to database: {save_message}"
            })
        
        logger.info(f"✅ Job successfully scraped and saved: {job_data['title']}")
        
        return jsonify({
            "success": True,
            "data": job_data,
            "message": save_message,
            "scraped_at": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"❌ Error in scrape endpoint: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "job_url": request.json.get('job_url', 'unknown')
        }), 500


@app.route('/jobs', methods=['GET'])
def get_jobs():
    """Get recent jobs from database"""
    try:
        limit = min(int(request.args.get('limit', 10)), 100)  # Max 100 jobs
        skip = int(request.args.get('skip', 0))
        
        result = db_manager.get_jobs(limit=limit, skip=skip)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "available_endpoints": {
            "POST /scrape": "Scrape a job URL",
            "GET /health": "Health check",
            "GET /jobs": "Get recent jobs"
        }
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


def main():
    """Main function to start the API server"""
    print("🚀 Starting Job Scraper API Server")
    print("="*50)
    print(f"📍 MongoDB URI: {db_manager.client.address if db_manager.client else 'Not connected'}")
    print(f"📊 Database: {db_manager.db.name if db_manager.client else 'Not connected'}")
    print(f"📁 Collection: {db_manager.collection.name if db_manager.client else 'Not connected'}")
    print("="*50)
    print("🔗 Available endpoints:")
    print("  POST /scrape - Scrape job from URL")
    print("  GET /health - Health check")
    print("  GET /jobs - Get recent jobs")
    print("="*50)
    
    # Start the server
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG_MODE)


if __name__ == '__main__':
    main()
