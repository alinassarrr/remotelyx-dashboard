from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, Token
from app.core.security import verify_token

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer(auto_error=False)

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate):
	"""Create a new user account"""
	try:
		user_service = UserService()
		user = await user_service.create_user(user_data)
		return user
	except ValueError as e:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=str(e)
		)
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="Internal server error"
		)

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
	"""Authenticate user and return JWT token"""
	user_service = UserService()
	token = await user_service.authenticate_user(user_data)
	
	if not token:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect email or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	
	return {"access_token": token, "token_type": "bearer"}

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> dict:
	"""Get current user from JWT token (strict)"""
	token = credentials.credentials
	payload = verify_token(token)
	
	if payload is None:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Could not validate credentials",
			headers={"WWW-Authenticate": "Bearer"},
		)
	
	return payload

async def get_optional_user(credentials: HTTPAuthorizationCredentials | None = Depends(security)) -> dict:
	"""Allow requests without auth (single-user mode); if token provided, validate it."""
	if credentials is None:
		# Anonymous/default single-user
		return {"sub": "single-user@remotelyx.local", "role": "admin"}
	payload = verify_token(credentials.credentials)
	return payload or {"sub": "single-user@remotelyx.local", "role": "admin"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
	"""Get current user information"""
	user_service = UserService()
	user = await user_service.get_user_by_email(current_user["sub"])
	
	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found"
		)
	
	return user 