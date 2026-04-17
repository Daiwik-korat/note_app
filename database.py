from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv() 

MONGO_URI = os.getenv("MONGO_DB_CONNECTION_URL")

client = AsyncIOMotorClient(MONGO_URI)
db = client["notes_db"]
notes_collection = db["notes"]