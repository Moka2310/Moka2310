from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class KYCStatus(str, Enum):
    PENDING = "pending"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class TelegramLink(BaseModel):
    name: str
    url: str

class Formation(BaseModel):
    id: str
    title: str
    description: str
    price: float
    duration: str
    level: str
    image: str
    videoCount: int
    telegramLinks: List[TelegramLink]
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class User(BaseModel):
    id: str
    email: EmailStr
    passwordHash: str
    firstName: Optional[str] = ""
    lastName: Optional[str] = ""
    country: Optional[str] = ""
    phone: Optional[str] = ""
    kycStatus: KYCStatus = KYCStatus.PENDING
    kycSubmittedAt: Optional[datetime] = None
    kycReviewedAt: Optional[datetime] = None
    kycRejectionReason: Optional[str] = None
    role: UserRole = UserRole.USER
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    firstName: Optional[str]
    lastName: Optional[str]
    country: Optional[str]
    phone: Optional[str]
    kycStatus: str
    role: str

class KYCDocument(BaseModel):
    id: str
    userId: str
    documentType: str  # passport, idCard, proofOfResidence
    filename: str
    filepath: str
    uploadedAt: datetime = Field(default_factory=datetime.utcnow)

class KYCSubmission(BaseModel):
    firstName: str
    lastName: str
    country: str
    phone: str

class Purchase(BaseModel):
    id: str
    userId: str
    formationId: str
    formationTitle: str
    price: float
    paymentMethod: str  # stripe, paypal
    paymentIntentId: Optional[str] = None
    status: str  # pending, completed, failed
    purchaseDate: datetime = Field(default_factory=datetime.utcnow)

class PurchaseCreate(BaseModel):
    formationId: str
    paymentMethod: str

class Video(BaseModel):
    id: str
    formationId: str
    title: str
    description: Optional[str]
    url: str
    duration: str
    order: int
    createdAt: datetime = Field(default_factory=datetime.utcnow)