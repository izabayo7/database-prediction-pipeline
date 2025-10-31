from bson import ObjectId
from .database import db

job_details = db["job_details"]

def get_job_details():
    return list(job_details.find())

def create_job_detail(data: dict):
    result = job_details.insert_one(data)
    return job_details.find_one({"_id": result.inserted_id})

def update_job_detail(id: str, data: dict):
    job_details.update_one({"_id": ObjectId(id)}, {"$set": data})
    return job_details.find_one({"_id": ObjectId(id)})

def delete_job_detail(id: str):
    res = job_details.delete_one({"_id": ObjectId(id)})
    return res.deleted_count > 0
