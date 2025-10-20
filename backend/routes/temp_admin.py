"""
Endpoint temporaire pour promouvoir un utilisateur en admin
À SUPPRIMER APRÈS UTILISATION
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from dependencies import get_db

router = APIRouter()

class PromoteRequest(BaseModel):
    email: str
    secret_key: str  # Pour sécuriser l'endpoint

@router.post("/admin/promote-user")
async def promote_user_to_admin(
    request: PromoteRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Clé secrète simple pour sécuriser
    if request.secret_key != "tradalife-admin-promote-2025":
        raise HTTPException(status_code=403, detail="Invalid secret key")
    
    # Trouver l'utilisateur
    user = await db.users.find_one({"email": request.email})
    
    if not user:
        raise HTTPException(status_code=404, detail=f"User {request.email} not found")
    
    # Promouvoir en admin
    result = await db.users.update_one(
        {"email": request.email},
        {"$set": {"role": "admin"}}
    )
    
    return {
        "success": True,
        "message": f"User {request.email} promoted to admin",
        "email": request.email,
        "previous_role": user.get("role", "user"),
        "new_role": "admin"
    }
