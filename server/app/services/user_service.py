from typing import Optional
from datetime import datetime
from app.core.database import get_collection
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user_model import UserModel
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from bson import ObjectId

class UserService:
    def __init__(self):
        self.collection = get_collection("users")

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user"""
        # Check if user already exists
        existing_user = await self.collection.find_one({"email": user_data.email})
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Create user document
        user_dict = user_data.dict()
        user_dict["password_hash"] = get_password_hash(user_data.password)
        user_dict["created_at"] = datetime.utcnow()
        user_dict["updated_at"] = datetime.utcnow()
        
        # Remove plain password
        del user_dict["password"]
        
        result = await self.collection.insert_one(user_dict)
        user_dict["_id"] = result.inserted_id
        
        return UserResponse(
            id=str(result.inserted_id),
            email=user_dict["email"],
            role=user_dict["role"],
            created_at=user_dict["created_at"],
            updated_at=user_dict["updated_at"]
        )

    async def authenticate_user(self, user_data: UserLogin) -> Optional[str]:
        """Authenticate user and return JWT token"""
        user = await self.collection.find_one({"email": user_data.email})
        if not user:
            return None
        
        if not verify_password(user_data.password, user["password_hash"]):
            return None
        
        # Create access token
        token_data = {"sub": user["email"], "role": user["role"]}
        access_token = create_access_token(data=token_data)
        return access_token

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get user by email"""
        user = await self.collection.find_one({"email": email})
        if not user:
            return None
        
        return UserResponse(
            id=str(user["_id"]),
            email=user["email"],
            role=user["role"],
            created_at=user["created_at"],
            updated_at=user["updated_at"]
        )

    async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Get user by ID"""
        try:
            user = await self.collection.find_one({"_id": ObjectId(user_id)})
            if not user:
                return None
            
            return UserResponse(
                id=str(user["_id"]),
                email=user["email"],
                role=user["role"],
                created_at=user["created_at"],
                updated_at=user["updated_at"]
            )
        except:
            return None 