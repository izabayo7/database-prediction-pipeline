from bson import ObjectId
from ..mongo_database import mongo_db as db

job_details = db["job_details"]

def get_job_details(skip=0, limit=10):
    return list(job_details.find().skip(skip).limit(limit))

def create_job_detail(data: dict):
    result = job_details.insert_one(data)
    return job_details.find_one({"_id": result.inserted_id})

def update_job_detail(id: str, data: dict):
    job_details.update_one({"_id": ObjectId(id)}, {"$set": data})
    return job_details.find_one({"_id": ObjectId(id)})

def delete_job_detail(id: str):
    res = job_details.delete_one({"_id": ObjectId(id)})
    return res.deleted_count > 0
