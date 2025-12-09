import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

MONGO_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME", "quiz_db")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]
quizzes_collection = db.get_collection("quizzes")

async def get_quiz_by_id(quiz_id: str):
    try:
        oid = ObjectId(quiz_id)
        return await quizzes_collection.find_one({"_id": oid})
    except:
        return None