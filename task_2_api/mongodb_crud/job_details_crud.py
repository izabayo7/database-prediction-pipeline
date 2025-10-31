from bson import ObjectId
from ..mongo_database import mongo_db as db

collection = db["job_details"]

def serialize_job_detail(job):
    if not job:
        return None
    job["job_id"] = str(job.pop("_id"))
    return job


def create_job_detail(data: dict):
    result = collection.insert_one(data)
    return serialize_job_detail(collection.find_one({"_id": result.inserted_id}))


def get_job_details(skip=0, limit=10):
    jobs = list(collection.find().skip(skip).limit(limit))
    return [serialize_job_detail(job) for job in jobs]


def get_job_detail(id: str):
    return serialize_job_detail(collection.find_one({"_id": ObjectId(id)}))


def update_job_detail(id: str, data: dict):
    collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    return serialize_job_detail(collection.find_one({"_id": ObjectId(id)}))


def delete_job_detail(id: str):
    result = collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
