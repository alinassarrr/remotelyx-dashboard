from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId
from app.models.user_model import PyObjectId

class ActivityLogModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    event: str = Field(..., index=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    job_id: Optional[PyObjectId] = None
    user_id: Optional[PyObjectId] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "event": "new_job_added",
                "timestamp": "2025-01-16T10:00:00Z",
                "job_id": "507f1f77bcf86cd799439011",
                "user_id": None,
                "details": {"source": "scraper", "company": "Tech Corp"},
                "created_at": "2025-01-16T10:00:00Z"
            }
        }
    } 