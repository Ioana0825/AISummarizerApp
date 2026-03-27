from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
MONGO_DB_NAME = "summarizer"

client = AsyncIOMotorClient(MONGO_URL)
mongo_db = client[MONGO_DB_NAME]

summaries_collection = mongo_db["summaries"]

def get_mongo_db():
    return mongo_db
