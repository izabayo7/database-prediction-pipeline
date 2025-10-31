from bson import ObjectId
from ..mongo_database import mongo_db as db

departments = db["departments"]

def serialize_department(dept):
    """Convert Mongo ObjectId to str for FastAPI/Pydantic."""
    if not dept:
        return None
    dept["department_id"] = str(dept.pop("_id")) 
    return dept

def get_departments(skip=0, limit=10):
    results = list(departments.find().skip(skip).limit(limit))
    return [serialize_department(d) for d in results]

def get_department(id: str):
    return serialize_department(departments.find_one({"_id": ObjectId(id)}))

def create_department(data: dict):
    result = departments.insert_one(data)
    return serialize_department(departments.find_one({"_id": result.inserted_id}))

def update_department(id: str, data: dict):
    departments.update_one({"_id": ObjectId(id)}, {"$set": data})
    return serialize_department(departments.find_one({"_id": ObjectId(id)}))

def delete_department(id: str):
    result = departments.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
