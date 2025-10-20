import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

# Configuration
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "tradalife")

async def update_testimonials():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Update all testimonials to add order field
    result = await db.testimonials.update_many(
        {'order': {'$exists': False}},
        {'$set': {'order': 0}}
    )
    print(f'✅ {result.modified_count} témoignages mis à jour avec le champ order')
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_testimonials())
