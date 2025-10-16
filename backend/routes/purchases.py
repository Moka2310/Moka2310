from fastapi import APIRouter, HTTPException, Depends
from models import Purchase, PurchaseCreate, User
from dependencies import get_db, get_current_user
from payment_service import StripePayment, PayPalPayment
from email_service import email_service
import uuid
from datetime import datetime
from typing import List

router = APIRouter(prefix="/purchases", tags=["Purchases"])

@router.post("/create")
async def create_purchase(purchase_data: PurchaseCreate, current_user: User = Depends(get_current_user)):
    db = get_db()
    
    # Get formation details
    formation = await db.formations.find_one({"id": purchase_data.formationId})
    if not formation:
        raise HTTPException(status_code=404, detail="Formation not found")
    
    # Check if user already purchased this formation
    existing_purchase = await db.purchases.find_one({
        "userId": current_user.id,
        "formationId": purchase_data.formationId,
        "status": "completed"
    })
    
    if existing_purchase:
        raise HTTPException(status_code=400, detail="You already own this formation")
    
    # Create purchase
    purchase = Purchase(
        id=str(uuid.uuid4()),
        userId=current_user.id,
        formationId=purchase_data.formationId,
        formationTitle=formation["title"],
        price=formation["price"],
        paymentMethod=purchase_data.paymentMethod,
        status="pending",
        purchaseDate=datetime.utcnow()
    )
    
    await db.purchases.insert_one(purchase.dict())
    
    # Create payment intent based on method
    if purchase_data.paymentMethod == "stripe":
        payment_result = await StripePayment.create_payment_intent(
            amount=formation["price"],
            currency="cad",
            metadata={
                "purchase_id": purchase.id,
                "formation_id": formation["id"],
                "user_id": current_user.id
            }
        )
        
        if payment_result["success"]:
            # Update purchase with payment intent ID
            await db.purchases.update_one(
                {"id": purchase.id},
                {"$set": {"paymentIntentId": payment_result["payment_intent_id"]}}
            )
            
            return {
                "purchaseId": purchase.id,
                "amount": purchase.price,
                "status": "pending",
                "clientSecret": payment_result["client_secret"],
                "paymentMethod": "stripe"
            }
        else:
            # Delete the purchase if payment failed
            await db.purchases.delete_one({"id": purchase.id})
            raise HTTPException(status_code=400, detail=f"Payment failed: {payment_result['error']}")
    
    elif purchase_data.paymentMethod == "paypal":
        payment_result = await PayPalPayment.create_payment(
            amount=formation["price"],
            currency="CAD",
            description=formation["title"]
        )
        
        if payment_result["success"]:
            # Update purchase with PayPal payment ID
            await db.purchases.update_one(
                {"id": purchase.id},
                {"$set": {"paymentIntentId": payment_result["payment_id"]}}
            )
            
            return {
                "purchaseId": purchase.id,
                "amount": purchase.price,
                "status": "pending",
                "approvalUrl": payment_result["approval_url"],
                "paymentMethod": "paypal"
            }
        else:
            raise HTTPException(status_code=400, detail=payment_result["error"])
    
    else:
        raise HTTPException(status_code=400, detail="Invalid payment method")

@router.post("/confirm/{purchase_id}")
async def confirm_purchase(purchase_id: str, current_user: User = Depends(get_current_user)):
    db = get_db()
    
    # Find purchase
    purchase = await db.purchases.find_one({"id": purchase_id, "userId": current_user.id})
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    
    # Update purchase status
    await db.purchases.update_one(
        {"id": purchase_id},
        {"$set": {"status": "completed"}}
    )
    
    # Get formation details
    formation = await db.formations.find_one({"id": purchase["formationId"]})
    
    # Send confirmation email
    await email_service.send_purchase_confirmation(
        current_user.email,
        formation["title"],
        purchase["price"]
    )
    
    return {
        "success": True,
        "message": "Purchase confirmed! Please complete your KYC to access the formation."
    }

@router.get("/my-purchases", response_model=List[Purchase])
async def get_my_purchases(current_user: User = Depends(get_current_user)):
    db = get_db()
    purchases = await db.purchases.find({"userId": current_user.id}).to_list(100)
    return [Purchase(**p) for p in purchases]