"""
Debug: test direct de mise à jour MongoDB
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

async def test_update():
    MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    DB_NAME = os.environ.get('DB_NAME', 'tradalife')
    
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Test avec Kevin A.
    print("Test de mise à jour sur Kevin A.:")
    result = await db.testimonials.update_one(
        {"userName": "Kevin A."},
        {"$set": {
            "comment_fr": "TEST FR",
            "comment_en": "TEST EN"
        }}
    )
    
    print(f"Matched: {result.matched_count}")
    print(f"Modified: {result.modified_count}")
    
    # Vérifier
    doc = await db.testimonials.find_one({"userName": "Kevin A."})
    if doc:
        print(f"Comment FR: {doc.get('comment_fr', 'N/A')}")
        print(f"Comment EN: {doc.get('comment_en', 'N/A')}")
    
    client.close()

asyncio.run(test_update())
