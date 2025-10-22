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

class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    PAST_DUE = "past_due"  # Paiement échoué, période de grâce
    CANCELED = "canceled"
    INCOMPLETE = "incomplete"  # Paiement initial en attente

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
    telegramUsername: Optional[str] = None  # Pour gérer l'accès aux canaux
    kycStatus: KYCStatus = KYCStatus.PENDING
    kycSubmittedAt: Optional[datetime] = None
    kycReviewedAt: Optional[datetime] = None
    kycRejectionReason: Optional[str] = None
    role: UserRole = UserRole.USER
    # Champs d'abonnement
    subscriptionId: Optional[str] = None  # Stripe Subscription ID
    subscriptionStatus: Optional[SubscriptionStatus] = None
    subscriptionStartDate: Optional[datetime] = None
    subscriptionEndDate: Optional[datetime] = None
    lastPaymentDate: Optional[datetime] = None
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
    telegramUsername: Optional[str] = None
    kycStatus: str
    role: str
    subscriptionStatus: Optional[str] = None
    subscriptionEndDate: Optional[datetime] = None

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
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class TestimonialStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Testimonial(BaseModel):
    id: str
    userId: str
    userName: str  # First + Last name
    country: str
    rating: int = Field(ge=1, le=5)  # 1 to 5 stars
    comment: str
    status: TestimonialStatus = TestimonialStatus.PENDING
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    reviewedAt: Optional[datetime] = None

class TestimonialCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str
    country: str

class TestimonialResponse(BaseModel):
    id: str
    userName: str
    country: str
    rating: int
    comment: str
    comment_fr: str = ""
    comment_en: str = ""
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    order: int = 0

class Subscription(BaseModel):
    id: str
    userId: str
    stripeSubscriptionId: str
    stripeCustomerId: str
    status: SubscriptionStatus
    priceId: str  # Stripe Price ID
    currentPeriodStart: datetime
    currentPeriodEnd: datetime
    cancelAtPeriodEnd: bool = False
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class SubscriptionCreate(BaseModel):
    telegramUsername: str
    paymentMethodId: str  # Stripe Payment Method ID

class SubscriptionResponse(BaseModel):
    id: str
    status: str
    currentPeriodEnd: datetime
    cancelAtPeriodEnd: bool


class BotPreorderStatus(str, Enum):
    PENDING_PAYMENT = "pending_payment"  # En attente de paiement
    PAID = "paid"  # Payé, en attente de livraison
    DELIVERED = "delivered"  # Bot livré au client
    REFUNDED = "refunded"  # Remboursé

class BotPreorder(BaseModel):
    id: str
    userId: str
    userEmail: str
    price: float = 300.0  # Prix en CAD
    status: BotPreorderStatus = BotPreorderStatus.PENDING_PAYMENT
    paymentMethod: str  # "stripe" ou "paypal"
    stripePaymentIntentId: Optional[str] = None
    paypalOrderId: Optional[str] = None
    deliveredAt: Optional[datetime] = None
    downloadLink: Optional[str] = None  # Lien de téléchargement une fois disponible
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class BotPreorderCreate(BaseModel):
    paymentMethod: str  # "stripe" ou "paypal"

class BotPreorderResponse(BaseModel):
    id: str
    price: float
    status: str
    createdAt: datetime
    deliveredAt: Optional[datetime] = None
    downloadLink: Optional[str] = None

    pricePerMonth: float = 150.0