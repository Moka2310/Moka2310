from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path

# Import routes
from routes import auth, formations, purchases, kyc, admin, testimonials, chat, temp_admin, telegram, subscriptions

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'tradalife')]

# Create the main app without a prefix
app = FastAPI(title="Tradalife API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Health check endpoint
@api_router.get("/")
async def root():
    return {"message": "Tradalife API is running", "status": "ok"}

# Include all route modules
api_router.include_router(auth.router)
api_router.include_router(formations.router)
api_router.include_router(purchases.router)
api_router.include_router(kyc.router)
api_router.include_router(admin.router)
api_router.include_router(testimonials.router)
api_router.include_router(chat.router)
api_router.include_router(temp_admin.router)
api_router.include_router(telegram.router)
api_router.include_router(subscriptions.router)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Run migrations on startup"""
    try:
        from pymongo import MongoClient
        MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        mongo_client = MongoClient(MONGO_URL)
        db_migrate = mongo_client.tradalife
        
        # Migration: Supprimer formation 1799 et mettre à jour images
        db_migrate.formations.delete_many({"price": 1799.0})
        db_migrate.formations.update_many({"price": 1100.0}, {"$set": {"image": "https://i.imgur.com/0wGvLuk.jpg"}})
        db_migrate.formations.update_many({"price": 700.0}, {"$set": {"image": "https://i.imgur.com/CcllRfh.jpg"}})
        
        mongo_client.close()
        logger.info("✅ Migrations executed successfully")
    except Exception as e:
        logger.error(f"❌ Migration error: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()