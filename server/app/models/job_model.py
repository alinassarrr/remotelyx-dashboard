from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId
from app.models.user_model import PyObjectId

class JobModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(..., index=True)
    company: str = Field(..., index=True)
    location: str = Field(..., index=True)
    type: str = Field(..., pattern="^(remote|hybrid|onsite)$")
    seniority: str = Field(..., pattern="^(junior|mid|senior)$")
    salary_min: int = Field(..., ge=0)
    salary_max: int = Field(..., ge=0)
    skills: List[str] = Field(default_factory=list, index=True)
    posting_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="new", pattern="^(new|analyzed|matched|closed)$")
    days_to_fill: Optional[int] = None
    matched_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "title": "Backend Engineer",
                "company": "Tech Corp",
                "location": "Remote",
                "type": "remote",
                "seniority": "senior",
                "salary_min": 80000,
                "salary_max": 120000,
                "skills": ["Python", "FastAPI", "MongoDB"],
                "posting_date": "2025-01-16T10:00:00Z",
                "status": "new",
                "days_to_fill": None,
                "matched_date": None,
                "created_at": "2025-01-16T10:00:00Z",
                "updated_at": "2025-01-16T10:00:00Z"
            }
        }
    } 