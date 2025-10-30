from fastapi import APIRouter, HTTPException, Depends
from models import UserCreate, UserLogin, UserResponse, User
from auth_utils import verify_password, get_password_hash, create_access_token
from dependencies import get_db, get_current_user
from email_service import email_service
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
    
    # Créer nouvel utilisateur
    user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        passwordHash=get_password_hash(user_data.password),
        createdAt=datetime.utcnow()
    )
    
    await db.users.insert_one(user.dict())
    
    # Gérer le parrainage si un code est fourni
    if user_data.referralCode:
        # Vérifier si le code existe
        referrer = await db.users.find_one({"referralCode": user_data.referralCode})
        if referrer:
            # Enregistrer le code dans le profil du filleul
            await db.users.update_one(
                {"id": user.id},
                {"$set": {"referredBy": user_data.referralCode}}
            )
            
            # Créer l'entrée de parrainage
            from models import Referral, ReferralStatus
            referral = Referral(
                id=str(uuid.uuid4()),
                referrerId=referrer['id'],
                referrerEmail=referrer['email'],
                referrerName=f"{referrer.get('firstName', '')} {referrer.get('lastName', '')}".strip() or referrer['email'],
                referralCode=user_data.referralCode,
                referredUserId=user.id,
                referredUserEmail=user.email,
                status=ReferralStatus.PENDING,
                createdAt=datetime.utcnow(),
                updatedAt=datetime.utcnow()
            )
            
            await db.referrals.insert_one(referral.dict())
            print(f"✅ Referral created: {referrer['email']} -> {user.email}")
    
    # Send welcome email
    await email_service.send_welcome_email(user.email)
    
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
    
    # Transform MongoDB document to match User model
    if 'userId' in user_dict:
        user_dict['id'] = user_dict.pop('userId')
    user_dict.pop('_id', None)  # Remove MongoDB ObjectId
    
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

@router.delete("/delete-account")
async def delete_account(current_user: User = Depends(get_current_user)):
    """
    Delete user account and all associated data (GDPR compliance)
    """
    from email_service import email_service
    from datetime import datetime, timezone
    
    db = get_db()
    user_id = current_user.id
    user_email = current_user.email
    user_name = f"{current_user.firstName} {current_user.lastName}".strip()
    
    try:
        # 1. Delete KYC documents
        await db.kyc_documents.delete_many({"userId": user_id})
        
        # 2. Delete purchases
        await db.purchases.delete_many({"userId": user_id})
        
        # 3. Delete testimonials
        await db.testimonials.delete_many({"userId": user_id})
        
        # 4. Log deletion for compliance
        deletion_log = {
            "userId": user_id,
            "email": user_email,
            "name": user_name,
            "deletedAt": datetime.now(timezone.utc).isoformat(),
            "reason": "user_request"
        }
        await db.deletion_logs.insert_one(deletion_log)
        
        # 5. Delete user account
        await db.users.delete_one({"id": user_id})
        
        # 6. Send confirmation email
        await email_service.send_account_deletion_confirmation(user_email, user_name)
        
        return {
            "success": True,
            "message": "Account and all associated data have been permanently deleted"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete account: {str(e)}"
        )


# Modèles pour la réinitialisation du mot de passe
from pydantic import BaseModel, EmailStr

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    newPassword: str

@router.post("/forgot-password")
async def forgot_password(request: PasswordResetRequest):
    """
    Demander la réinitialisation du mot de passe
    Envoie un email avec un lien de réinitialisation
    """
    db = get_db()
    
    try:
        # Vérifier si l'utilisateur existe
        user = await db.users.find_one({"email": request.email})
        
        # Pour la sécurité, on retourne toujours succès même si l'email n'existe pas
        # (évite l'énumération des comptes)
        if not user:
            return {
                "success": True,
                "message": "Si cet email existe, un lien de réinitialisation a été envoyé"
            }
        
        # Générer un token de réinitialisation
        reset_token = str(uuid.uuid4())
        reset_expiry = datetime.utcnow()
        
        # Sauvegarder le token dans la base de données
        await db.password_resets.insert_one({
            "token": reset_token,
            "userId": user["id"],
            "email": user["email"],
            "createdAt": reset_expiry.isoformat(),
            "used": False
        })
        
        # Créer le lien de réinitialisation
        frontend_url = "https://edushop-portal.emergent.host"  # URL de production
        reset_link = f"{frontend_url}/reset-password?token={reset_token}"
        
        # Envoyer l'email
        await email_service.send_password_reset_email(
            user["email"],
            reset_link,
            user.get("firstName", "")
        )
        
        return {
            "success": True,
            "message": "Si cet email existe, un lien de réinitialisation a été envoyé"
        }
        
    except Exception as e:
        # Ne pas révéler les détails de l'erreur pour la sécurité
        return {
            "success": True,
            "message": "Si cet email existe, un lien de réinitialisation a été envoyé"
        }

@router.post("/reset-password")
async def reset_password(reset_data: PasswordReset):
    """
    Réinitialiser le mot de passe avec le token
    """
    db = get_db()
    
    try:
        # Vérifier le token
        reset_record = await db.password_resets.find_one({
            "token": reset_data.token,
            "used": False
        })
        
        if not reset_record:
            raise HTTPException(
                status_code=400,
                detail="Token invalide ou expiré"
            )
        
        # Vérifier si le token a moins de 1 heure
        from datetime import timedelta
        created_at = datetime.fromisoformat(reset_record["createdAt"])
        if datetime.utcnow() - created_at > timedelta(hours=1):
            raise HTTPException(
                status_code=400,
                detail="Le lien de réinitialisation a expiré. Veuillez en demander un nouveau."
            )
        
        # Mettre à jour le mot de passe
        new_password_hash = get_password_hash(reset_data.newPassword)
        
        result = await db.users.update_one(
            {"id": reset_record["userId"]},
            {"$set": {"passwordHash": new_password_hash}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=500,
                detail="Erreur lors de la mise à jour du mot de passe"
            )
        
        # Marquer le token comme utilisé
        await db.password_resets.update_one(
            {"token": reset_data.token},
            {"$set": {"used": True, "usedAt": datetime.utcnow().isoformat()}}
        )
        
        return {
            "success": True,
            "message": "Mot de passe réinitialisé avec succès"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la réinitialisation: {str(e)}"
        )
