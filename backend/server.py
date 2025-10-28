from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path

# Import routes
from routes import auth, formations, purchases, kyc, admin, testimonials, chat, temp_admin, telegram, subscriptions, migrations, bot_preorders, trading_contest, members, bonus_announcements, referrals, tradabot

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
api_router.include_router(migrations.router)
api_router.include_router(bot_preorders.router)
api_router.include_router(trading_contest.router)
api_router.include_router(members.router)
api_router.include_router(bonus_announcements.router)
api_router.include_router(referrals.router)
api_router.include_router(tradabot.router)

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
        from datetime import datetime
        import uuid
        
        MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        DB_NAME = os.environ.get('DB_NAME', 'tradalife')
        logger.info(f"🔗 Connecting to MongoDB for migrations...")
        mongo_client = MongoClient(MONGO_URL)
        db_migrate = mongo_client[DB_NAME]
        
        # Log formations BEFORE migration
        formations_before = list(db_migrate.formations.find({}, {"title": 1, "price": 1, "image": 1}))
        logger.info(f"📋 Formations BEFORE migration: {len(formations_before)}")
        for f in formations_before:
            logger.info(f"  - {f.get('title', 'N/A')} ({f.get('price', 'N/A')} CAD): {f.get('image', 'N/A')[:50]}")
        
        # Migration: Supprimer formation 1799 et mettre à jour images
        result_delete = db_migrate.formations.delete_many({"price": 1799.0})
        logger.info(f"🗑️ Deleted formations with price 1799: {result_delete.deleted_count}")
        
        result_ultra = db_migrate.formations.update_many(
            {"price": 1100.0}, 
            {"$set": {"image": "https://i.imgur.com/0wGvLuk.jpg"}}
        )
        logger.info(f"🔄 Updated Ultra formation (1100 CAD): {result_ultra.modified_count} modified")
        
        result_premium = db_migrate.formations.update_many(
            {"price": 700.0}, 
            {"$set": {"image": "https://i.imgur.com/CcllRfh.jpg"}}
        )
        logger.info(f"🔄 Updated Premium formation (700 CAD): {result_premium.modified_count} modified")
        
        # Log formations AFTER migration
        formations_after = list(db_migrate.formations.find({}, {"title": 1, "price": 1, "image": 1}))
        logger.info(f"📋 Formations AFTER migration: {len(formations_after)}")
        for f in formations_after:
            logger.info(f"  - {f.get('title', 'N/A')} ({f.get('price', 'N/A')} CAD): {f.get('image', 'N/A')[:50]}")
        
        # Migration BOT: Initialiser 21 précommandes factices pour afficher 9/30
        logger.info("🤖 Checking bot preorders...")
        current_preorder_count = db_migrate.bot_preorders.count_documents({
            "status": {"$in": ["pending_payment", "paid"]}
        })
        logger.info(f"📊 Current bot preorders: {current_preorder_count}")
        
        target_preorder_count = 21
        if current_preorder_count < target_preorder_count:
            preorders_to_create = target_preorder_count - current_preorder_count
            logger.info(f"➕ Creating {preorders_to_create} fake bot preorders...")
            
            for i in range(preorders_to_create):
                fake_preorder = {
                    "id": str(uuid.uuid4()),
                    "userId": f"fake_user_{current_preorder_count + i}",
                    "userEmail": f"fake_{current_preorder_count + i}@example.com",
                    "price": 300.0,
                    "status": "paid",
                    "paymentMethod": "stripe",
                    "stripePaymentIntentId": f"fake_pi_{current_preorder_count + i}",
                    "createdAt": datetime.utcnow(),
                    "updatedAt": datetime.utcnow()
                }
                db_migrate.bot_preorders.insert_one(fake_preorder)
            
            final_count = db_migrate.bot_preorders.count_documents({
                "status": {"$in": ["pending_payment", "paid"]}
            })
            logger.info(f"✅ Bot preorders initialized: {final_count} sold, {30 - final_count} available")
        else:
            logger.info(f"✅ Bot preorders already initialized: {current_preorder_count} sold, {30 - current_preorder_count} available")
        
        mongo_client.close()
        logger.info("✅ All migrations executed successfully")
    except Exception as e:
        logger.error(f"❌ Migration error: {e}", exc_info=True)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()