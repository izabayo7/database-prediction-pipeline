from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")

if not MONGO_URL or not MONGO_DB:
    raise ValueError("MongoDB environment variables are missing. Check your .env file.")

# Connect to MongoDB
client = MongoClient(MONGO_URL)

# Select the database
mongo_db = client[MONGO_DB]

print(f"✅ Connected to MongoDB database: {MONGO_DB}")
