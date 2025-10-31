from bson import ObjectId
from .database import db

departments = db["departments"]

def get_employees(skip=0, limit=10):
    return list(employees.find().skip(skip).limit(limit))

def get_employee(id: str):
    return employees.find_one({"_id": ObjectId(id)})

def create_employee(data: dict):
    result = employees.insert_one(data)
    return employees.find_one({"_id": result.inserted_id})

def update_employee(id: str, data: dict):
    employees.update_one({"_id": ObjectId(id)}, {"$set": data})
    return employees.find_one({"_id": ObjectId(id)})

def delete_employee(id: str):
    res = employees.delete_one({"_id": ObjectId(id)})
    return res.deleted_count > 0


# ============ DEPARTMENTS ============
def get_departments():
    return list(departments.find())

def create_department(data: dict):
    result = departments.insert_one(data)
    return departments.find_one({"_id": result.inserted_id})