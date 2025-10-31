from bson import ObjectId
from datetime import datetime


def get_predictions(mongo_db, skip: int = 0, limit: int = 10, filters: dict = None):
    """
    Get predictions with pagination and optional filters.
    """
    predictions_collection = mongo_db["predictions"]
    
    # Apply filters if provided
    query = filters if filters else {}
    
    # Query with pagination
    cursor = predictions_collection.find(query).sort("prediction_date", -1).skip(skip).limit(limit)
    data = list(cursor)
    
    # Convert ObjectId to string
    for item in data:
        if "_id" in item:
            item["_id"] = str(item["_id"])
    
    return data


def get_prediction(mongo_db, prediction_id: str):
    """
    Get a single prediction by ID.
    """
    predictions_collection = mongo_db["predictions"]
    prediction = predictions_collection.find_one({"_id": ObjectId(prediction_id)})
    
    if prediction:
        prediction["_id"] = str(prediction["_id"])
    
    return prediction


def create_prediction(mongo_db, prediction_data: dict):
    """
    Create a new prediction record in MongoDB.
    No foreign key constraints - we just store the employee_number.
    """
    predictions_collection = mongo_db["predictions"]
    
    # Ensure prediction_date is set
    if "prediction_date" not in prediction_data:
        prediction_data["prediction_date"] = datetime.utcnow()
    
    # Insert the prediction
    result = predictions_collection.insert_one(prediction_data)
    
    # Fetch and return the created prediction
    new_prediction = predictions_collection.find_one({"_id": result.inserted_id})
    
    if new_prediction:
        new_prediction["_id"] = str(new_prediction["_id"])
    
    return new_prediction


def get_predictions_by_employee(mongo_db, employee_number: int, limit: int = 10):
    """
    Get predictions for a specific employee number.
    """
    predictions_collection = mongo_db["predictions"]
    
    cursor = predictions_collection.find(
        {"employee_number": employee_number}
    ).sort("prediction_date", -1).limit(limit)
    
    data = list(cursor)
    
    # Convert ObjectId to string
    for item in data:
        if "_id" in item:
            item["_id"] = str(item["_id"])
    
    return data

