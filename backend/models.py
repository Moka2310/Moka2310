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
    paymentMethodId: Optional[str] = None  # Stripe Payment Method ID (optionnel pour PayPal)
    paymentMethod: Optional[str] = "stripe"  # "stripe" ou "paypal"

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

class TradingContestParticipant(BaseModel):
    id: str
    firstName: str
    lastName: str
    totalTrades: int  # Nombre de trades ouverts
    winningTrades: int  # Trades gagnants
    winRate: float = 0.0  # Pourcentage calculé automatiquement
    date: datetime  # Date du concours
    rank: int = 0  # Classement calculé automatiquement
    isActive: bool = True  # Afficher ou masquer
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class TradingContestCreate(BaseModel):
    firstName: str
    lastName: str
    totalTrades: int
    winningTrades: int
    date: datetime


# ===== BONUS ANNOUNCEMENTS MODELS =====
class BonusAnnouncement(BaseModel):
    id: str
    titleFr: str  # Titre en français
    titleEn: str  # Titre en anglais
    descriptionFr: Optional[str] = None  # Description en français
    descriptionEn: Optional[str] = None  # Description en anglais
    imageUrl: str  # URL de l'image
    linkUrl: Optional[str] = None  # Lien optionnel vers une page
    isActive: bool = True  # Afficher ou masquer
    order: int = 0  # Ordre d'affichage
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class BonusAnnouncementCreate(BaseModel):
    titleFr: str
    titleEn: str
    descriptionFr: Optional[str] = None
    descriptionEn: Optional[str] = None
    imageUrl: str
    linkUrl: Optional[str] = None
    order: Optional[int] = 0

class BonusAnnouncementUpdate(BaseModel):
    titleFr: Optional[str] = None
    titleEn: Optional[str] = None
    descriptionFr: Optional[str] = None
    descriptionEn: Optional[str] = None
    imageUrl: Optional[str] = None
    linkUrl: Optional[str] = None
    isActive: Optional[bool] = None
    order: Optional[int] = None


# ===== REFERRAL SYSTEM MODELS =====
class ReferralStatus(str, Enum):
    PENDING = "pending"  # Inscrit mais pas encore d'achat
    COMPLETED = "completed"  # Premier achat effectué
    REWARDED = "rewarded"  # Récompense versée

class Referral(BaseModel):
    id: str
    referrerId: str  # ID du parrain
    referrerEmail: str  # Email du parrain
    referrerName: str  # Nom du parrain pour affichage
    referralCode: str  # Code unique (nom-utilisateur)
    referredUserId: Optional[str] = None  # ID du filleul (rempli après inscription)
    referredUserEmail: Optional[str] = None  # Email du filleul
    status: ReferralStatus = ReferralStatus.PENDING
    purchaseType: Optional[str] = None  # Type d'achat: "formation", "bot", "subscription"
    purchaseAmount: Optional[float] = None  # Montant de l'achat
    rewardAmount: float = 200.0  # Montant de la récompense (200$ CAD)
    adminNotified: bool = False  # Notification admin envoyée
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    completedAt: Optional[datetime] = None  # Date du premier achat
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class ReferralCreate(BaseModel):
    referralCode: str  # Code du parrain

class TradingContestUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    totalTrades: Optional[int] = None
    winningTrades: Optional[int] = None
    date: Optional[datetime] = None
    isActive: Optional[bool] = None

class TradingContestResponse(BaseModel):
    id: str
    firstName: str
    lastName: str
    totalTrades: int
    winningTrades: int
    winRate: float
    date: datetime
    rank: int

    pricePerMonth: float = 150.0