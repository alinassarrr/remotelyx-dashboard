from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.controllers import auth_controller, job_controller, analytics_controller, scraper_controller

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="RemotelyX API - Job Market Analytics for Recruiters"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_controller.router, prefix=settings.API_V1_STR)
app.include_router(job_controller.router, prefix=settings.API_V1_STR)
app.include_router(analytics_controller.router, prefix=settings.API_V1_STR)
app.include_router(scraper_controller.router, prefix=settings.API_V1_STR)

# Startup event
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to RemotelyX API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "RemotelyX API"}
