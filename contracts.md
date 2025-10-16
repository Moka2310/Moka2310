# Contrats API - Tradalife Clone

## Architecture Backend

### Base de données MongoDB
- **users**: Comptes utilisateurs avec KYC
- **formations**: Catalogue de formations
- **purchases**: Historique des achats
- **kyc_documents**: Documents KYC uploadés

---

## 1. API Authentication

### POST /api/auth/register
**Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
**Response:**
```json
{
  "user": {
    "id": "...",
    "email": "...",
    "kycStatus": "pending"
  },
  "token": "jwt_token"
}
```

### POST /api/auth/login
**Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
**Response:**
```json
{
  "user": { ... },
  "token": "jwt_token"
}
```

### GET /api/auth/me
**Headers:** `Authorization: Bearer {token}`
**Response:** User object

---

## 2. API Formations

### GET /api/formations
**Response:**
```json
[
  {
    "id": "1",
    "title": "Formation Trading Crypto",
    "description": "...",
    "price": 299,
    "duration": "8 heures",
    "level": "Débutant",
    "image": "...",
    "videoCount": 12,
    "telegramLinks": [...]
  }
]
```

### GET /api/formations/:id
**Response:** Formation object

---

## 3. API Purchases & Checkout

### POST /api/checkout/create-payment-intent
**Body:**
```json
{
  "formationId": "1",
  "paymentMethod": "stripe" | "paypal"
}
```
**Response:**
```json
{
  "clientSecret": "stripe_client_secret",
  "purchaseId": "..."
}
```

### POST /api/checkout/confirm
**Body:**
```json
{
  "purchaseId": "...",
  "paymentIntentId": "...",
  "status": "success"
}
```
**Response:**
```json
{
  "success": true,
  "purchase": { ... }
}
```

### GET /api/purchases/my-purchases
**Headers:** `Authorization: Bearer {token}`
**Response:** Array of purchases

---

## 4. API KYC

### POST /api/kyc/submit
**Headers:** `Authorization: Bearer {token}`
**Body (multipart/form-data):**
```
firstName: "John"
lastName: "Doe"
country: "France"
phone: "+33612345678"
passport: File
idCard: File
proofOfResidence: File
```
**Response:**
```json
{
  "success": true,
  "kycStatus": "pending_review"
}
```

### GET /api/kyc/status
**Headers:** `Authorization: Bearer {token}`
**Response:**
```json
{
  "kycStatus": "pending" | "pending_review" | "approved" | "rejected",
  "submittedAt": "2025-01-15T...",
  "reviewedAt": "..."
}
```

---

## 5. API Admin (pour validation KYC)

### GET /api/admin/kyc-requests
**Headers:** `Authorization: Bearer {admin_token}`
**Response:** Array of pending KYC requests

### POST /api/admin/kyc-approve/:userId
**Headers:** `Authorization: Bearer {admin_token}`
**Response:**
```json
{
  "success": true,
  "user": { ... }
}
```

### POST /api/admin/kyc-reject/:userId
**Headers:** `Authorization: Bearer {admin_token}`
**Body:**
```json
{
  "reason": "Documents invalides"
}
```

---

## 6. API Videos (pour utilisateurs KYC approuvés)

### GET /api/videos/:formationId
**Headers:** `Authorization: Bearer {token}`
**Response:**
```json
{
  "videos": [
    {
      "id": "1",
      "title": "Introduction au Trading Crypto",
      "url": "/videos/formation1/video1.mp4",
      "duration": "15:30"
    }
  ]
}
```

---

## Intégrations requises

### Stripe
- API Key (sk_test_...)
- Webhook pour confirmation de paiement

### PayPal
- Client ID
- Client Secret
- Webhook pour confirmation de paiement

### Email (SMTP)
- Service: Gmail, SendGrid, ou autre
- Templates:
  - Confirmation d'inscription
  - Confirmation de paiement
  - KYC soumis
  - KYC approuvé
  - KYC rejeté

---

## Frontend Integration Points

### Remplacer mock data par API calls:
1. **mockData.js** → GET /api/formations
2. **AuthContext.jsx** → POST /api/auth/login, /api/auth/register, GET /api/auth/me
3. **Dashboard.jsx** → GET /api/purchases/my-purchases, POST /api/kyc/submit
4. **Checkout.jsx** → POST /api/checkout/create-payment-intent, POST /api/checkout/confirm

### localStorage usage:
- Store JWT token after login
- Add token to all authenticated requests

---

## Workflow complet

1. User s'inscrit → Email de bienvenue
2. User achète formation → Paiement Stripe/PayPal → Email de confirmation
3. User soumet KYC → Email "KYC reçu"
4. Admin valide KYC → Email "KYC approuvé" + accès formations
5. User accède vidéos + liens Telegram VIP
