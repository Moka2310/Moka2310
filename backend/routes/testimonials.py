from fastapi import APIRouter, HTTPException, Depends
from models import Testimonial, TestimonialCreate, TestimonialResponse, TestimonialStatus, User
from dependencies import get_db, get_current_user
import uuid
from datetime import datetime, timezone
from typing import List

router = APIRouter(prefix="/testimonials", tags=["Testimonials"])

@router.post("/submit")
async def submit_testimonial(
    testimonial_data: TestimonialCreate,
    current_user: User = Depends(get_current_user)
):
    """Submit a new testimonial (requires authentication)"""
    db = get_db()
    
    # Check if user already submitted a testimonial
    existing = await db.testimonials.find_one({"userId": current_user.id})
    if existing:
        raise HTTPException(status_code=400, detail="You have already submitted a testimonial")
    
    # Create testimonial
    testimonial = Testimonial(
        id=str(uuid.uuid4()),
        userId=current_user.id,
        userName=f"{current_user.firstName} {current_user.lastName}".strip() or "Anonymous",
        country=testimonial_data.country,
        rating=testimonial_data.rating,
        comment=testimonial_data.comment,
        status=TestimonialStatus.PENDING,
        createdAt=datetime.now(timezone.utc)
    )
    
    await db.testimonials.insert_one(testimonial.dict())
    
    return {"message": "Testimonial submitted successfully. It will be reviewed by our team."}

@router.get("/approved", response_model=List[TestimonialResponse])
async def get_approved_testimonials():
    """Get all approved testimonials (public endpoint)"""
    db = get_db()
    
    testimonials = await db.testimonials.find(
        {"status": TestimonialStatus.APPROVED.value}
    ).sort("createdAt", -1).to_list(length=100)
    
    return [
        TestimonialResponse(
            id=t["id"],
            userName=t["userName"],
            country=t["country"],
            rating=t["rating"],
            comment=t["comment"],
            createdAt=t["createdAt"]
        )
        for t in testimonials
    ]

@router.get("/my-testimonial")
async def get_my_testimonial(current_user: User = Depends(get_current_user)):
    """Get current user's testimonial"""
    db = get_db()
    
    testimonial = await db.testimonials.find_one({"userId": current_user.id})
    
    if not testimonial:
        return {"exists": False}
    
    return {
        "exists": True,
        "testimonial": {
            "id": testimonial["id"],
            "rating": testimonial["rating"],
            "comment": testimonial["comment"],
            "country": testimonial["country"],
            "status": testimonial["status"],
            "createdAt": testimonial["createdAt"]
        }
    }
