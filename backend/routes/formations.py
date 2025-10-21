from fastapi import APIRouter, HTTPException
from models import Formation, TelegramLink
from dependencies import get_db
from typing import List

router = APIRouter(prefix="/formations", tags=["Formations"])

@router.get("", response_model=List[Formation])
async def get_formations():
    """Get all formations from database"""
    db = get_db()
    formations = await db.formations.find().to_list(100)
    return [Formation(**f) for f in formations]

@router.get("/{formation_id}", response_model=Formation)
async def get_formation(formation_id: str):
    """Get a specific formation by ID"""
    db = get_db()
    formation = await db.formations.find_one({"id": formation_id})
    
    if not formation:
        raise HTTPException(status_code=404, detail="Formation not found")
    
    return Formation(**formation)
