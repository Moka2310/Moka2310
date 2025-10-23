from fastapi import Depends, HTTPException, status, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorClient
from models import User, UserRole
from auth_utils import decode_token
import os
from typing import Optional
import uuid
import aiofiles
from pathlib import Path

security = HTTPBearer()

# Get MongoDB client
def get_db():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'tradalife')]
    return db

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    db = get_db()
    user_dict = await db.users.find_one({"id": user_id})
    
    if user_dict is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return User(**user_dict)

async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

# Alias for compatibility
require_admin = get_current_admin


async def save_upload_file(upload_file: UploadFile, user_id: str, doc_type: str) -> tuple[str, str]:
    """Save uploaded file and return (filename, filepath)"""
    
    # Create uploads directory if it doesn't exist
    upload_dir = Path("/app/backend/uploads") / user_id
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    file_extension = Path(upload_file.filename).suffix
    unique_filename = f"{doc_type}_{uuid.uuid4()}{file_extension}"
    file_path = upload_dir / unique_filename
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        content = await upload_file.read()
        await f.write(content)
    
    return unique_filename, str(file_path)