from fastapi import APIRouter, HTTPException, Depends
from models import User, KYCStatus
from dependencies import get_db, get_current_admin
from email_service import email_service
from datetime import datetime
from typing import List

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/kyc-requests")
async def get_kyc_requests(current_admin: User = Depends(get_current_admin)):
    db = get_db()
    
    # Get all users with pending KYC
    users = await db.users.find({
        "kycStatus": KYCStatus.PENDING_REVIEW.value
    }).to_list(100)
    
    result = []
    for user_dict in users:
        # Get documents for this user
        documents = await db.kyc_documents.find({"userId": user_dict["id"]}).to_list(10)
        
        result.append({
            "user": {
                "id": user_dict["id"],
                "email": user_dict["email"],
                "firstName": user_dict.get("firstName", ""),
                "lastName": user_dict.get("lastName", ""),
                "country": user_dict.get("country", ""),
                "phone": user_dict.get("phone", ""),
                "kycSubmittedAt": user_dict.get("kycSubmittedAt")
            },
            "documents": documents
        })
    
    return result

@router.post("/kyc-approve/{user_id}")
async def approve_kyc(user_id: str, current_admin: User = Depends(get_current_admin)):
    db = get_db()
    
    # Find user
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's purchases to determine formations
    purchases = await db.purchases.find({"userId": user_id, "status": "confirmed"}).to_list(length=None)
    formation_ids = [p["formationId"] for p in purchases]
    
    # Get formation titles
    formation_titles = []
    if formation_ids:
        formations = await db.formations.find({"id": {"$in": formation_ids}}).to_list(length=None)
        formation_titles = [f["title"] for f in formations]
    
    # Update KYC status
    await db.users.update_one(
        {"id": user_id},
        {"$set": {
            "kycStatus": KYCStatus.APPROVED.value,
            "kycReviewedAt": datetime.utcnow(),
            "kycRejectionReason": None
        }}
    )
    
    # Send approval email with formations info
    await email_service.send_kyc_approved(user["email"], formation_titles)
    
    return {
        "success": True,
        "message": f"KYC approved for user {user['email']}"
    }

@router.post("/kyc-reject/{user_id}")
async def reject_kyc(user_id: str, reason: str, current_admin: User = Depends(get_current_admin)):
    db = get_db()
    
    # Find user
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update KYC status
    await db.users.update_one(
        {"id": user_id},
        {"$set": {
            "kycStatus": KYCStatus.REJECTED.value,
            "kycReviewedAt": datetime.utcnow(),
            "kycRejectionReason": reason
        }}
    )
    
    # Send rejection email
    await email_service.send_kyc_rejected(user["email"], reason)
    
    return {
        "success": True,
        "message": f"KYC rejected for user {user['email']}"
    }

@router.get("/stats")
async def get_admin_stats(current_admin: User = Depends(get_current_admin)):
    db = get_db()
    
    total_users = await db.users.count_documents({})
    pending_kyc = await db.users.count_documents({"kycStatus": KYCStatus.PENDING_REVIEW.value})
    approved_kyc = await db.users.count_documents({"kycStatus": KYCStatus.APPROVED.value})
    total_purchases = await db.purchases.count_documents({"status": "completed"})
    
    # Calculate total revenue
    purchases = await db.purchases.find({"status": "completed"}).to_list(10000)
    total_revenue = sum(p["price"] for p in purchases)
    
    return {
        "totalUsers": total_users,
        "pendingKyc": pending_kyc,
        "approvedKyc": approved_kyc,
        "totalPurchases": total_purchases,
        "totalRevenue": total_revenue
    }