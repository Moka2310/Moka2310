from fastapi import APIRouter, HTTPException, Depends
from models import UserCreate, UserLogin, UserResponse, User
from auth_utils import verify_password, get_password_hash, create_access_token
from dependencies import get_db, get_current_user
import uuid
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
async def register(user_data: UserCreate):
    db = get_db()
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        passwordHash=get_password_hash(user_data.password),
        createdAt=datetime.utcnow()
    )
    
    await db.users.insert_one(user.dict())
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    return {
        "user": UserResponse(
            id=user.id,
            email=user.email,
            firstName=user.firstName,
            lastName=user.lastName,
            country=user.country,
            phone=user.phone,
            kycStatus=user.kycStatus.value,
            role=user.role.value
        ),
        "token": access_token
    }

@router.post("/login")
async def login(credentials: UserLogin):
    db = get_db()
    
    # Find user
    user_dict = await db.users.find_one({"email": credentials.email})
    if not user_dict:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    user = User(**user_dict)
    
    # Verify password
    if not verify_password(credentials.password, user.passwordHash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    return {
        "user": UserResponse(
            id=user.id,
            email=user.email,
            firstName=user.firstName,
            lastName=user.lastName,
            country=user.country,
            phone=user.phone,
            kycStatus=user.kycStatus.value,
            role=user.role.value
        ),
        "token": access_token
    }

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        firstName=current_user.firstName,
        lastName=current_user.lastName,
        country=current_user.country,
        phone=current_user.phone,
        kycStatus=current_user.kycStatus.value,
        role=current_user.role.value
    )