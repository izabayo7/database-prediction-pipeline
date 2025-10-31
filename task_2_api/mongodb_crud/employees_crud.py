from bson import ObjectId

def get_employees(mongo_db, skip: int = 0, limit: int = 10, filters: dict = None):
    employees_collection = mongo_db["employees"]

    # Apply filters if provided
    query = filters if filters else {}

    # Query with pagination
    cursor = employees_collection.find(query).skip(skip).limit(limit)
    data = list(cursor)

    # Convert ObjectId to string
    for item in data:
        if "_id" in item:
            item["_id"] = str(item["_id"])

    return data


def get_employee(mongo_db, employee_id: str):
    employees_collection = mongo_db["employees"]
    employee = employees_collection.find_one({"_id": ObjectId(employee_id)})
    if employee:
        employee["_id"] = str(employee["_id"])
    return employee

def create_employee(mongo_db, employee_data: dict):
    employees_collection = mongo_db["employees"]

    # Auto-generate employee_number
    last = employees_collection.find_one(sort=[("employee_number", -1)])
    next_number = (last["employee_number"] + 1) if last and "employee_number" in last else 1
    employee_data["employee_number"] = next_number

    result = employees_collection.insert_one(employee_data)

    new_emp = employees_collection.find_one({"_id": result.inserted_id})
    new_emp["_id"] = str(new_emp["_id"])  # ✅ Make sure this line exists

    return new_emp

def update_employee(mongo_db, employee_id: str, update_data: dict):
    employees_collection = mongo_db["employees"]
    employees_collection.update_one({"_id": ObjectId(employee_id)}, {"$set": update_data})
    updated_emp = employees_collection.find_one({"_id": ObjectId(employee_id)})
    if updated_emp:
        updated_emp["_id"] = str(updated_emp["_id"])
    return updated_emp


def delete_employee(mongo_db, employee_id: str):
    employees_collection = mongo_db["employees"]
    result = employees_collection.delete_one({"_id": ObjectId(employee_id)})
    if result.deleted_count == 1:
        return {"message": f"Employee {employee_id} deleted successfully"}
    else:
        return {"message": f"Employee {employee_id} not found"}
