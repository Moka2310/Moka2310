from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from models import User, KYCStatus, KYCDocument
from dependencies import get_db, get_current_user, save_upload_file, get_current_admin
from email_service import email_service
import uuid
from datetime import datetime
from typing import List

router = APIRouter(prefix="/kyc", tags=["KYC"])

@router.post("/submit")
async def submit_kyc(
    firstName: str = Form(...),
    lastName: str = Form(...),
    country: str = Form(...),
    phone: str = Form(...),
    passport: UploadFile = File(...),
    idCard: UploadFile = File(...),
    proofOfResidence: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    db = get_db()
    
    # Save documents
    documents = []
    
    for upload_file, doc_type in [
        (passport, "passport"),
        (idCard, "idCard"),
        (proofOfResidence, "proofOfResidence")
    ]:
        filename, filepath = await save_upload_file(upload_file, current_user.id, doc_type)
        
        doc = KYCDocument(
            id=str(uuid.uuid4()),
            userId=current_user.id,
            documentType=doc_type,
            filename=filename,
            filepath=filepath,
            uploadedAt=datetime.utcnow()
        )
        
        await db.kyc_documents.insert_one(doc.dict())
        documents.append(doc)
    
    # Update user info
    await db.users.update_one(
        {"id": current_user.id},
        {"$set": {
            "firstName": firstName,
            "lastName": lastName,
            "country": country,
            "phone": phone,
            "kycStatus": KYCStatus.PENDING.value,
            "kycSubmittedAt": datetime.utcnow()
        }}
    )
    
    # Send confirmation email
    await email_service.send_kyc_submitted(current_user.email)
    
    return {
        "success": True,
        "kycStatus": KYCStatus.PENDING.value,
        "message": "KYC submitted successfully. You will receive an email once reviewed."
    }

@router.get("/status")
async def get_kyc_status(current_user: User = Depends(get_current_user)):
    return {
        "kycStatus": current_user.kycStatus.value,
        "submittedAt": current_user.kycSubmittedAt,
        "reviewedAt": current_user.kycReviewedAt,
        "rejectionReason": current_user.kycRejectionReason
    }

@router.get("/documents")
async def get_my_documents(current_user: User = Depends(get_current_user)):
    db = get_db()
    documents = await db.kyc_documents.find({"userId": current_user.id}).to_list(100)
    return [KYCDocument(**doc) for doc in documents]