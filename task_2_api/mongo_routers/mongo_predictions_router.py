from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime

from ..mongo_database import mongo_db
from ..mongodb_crud import predictions_crud as crud
from ..mongodb_schemas import Prediction, PredictionCreate

router = APIRouter(
    prefix="/mongo/predictions",
    tags=["Predictions (MongoDB)"]
)


@router.post("/", response_model=Prediction, status_code=201)
def create_prediction(prediction: PredictionCreate):
    """
    Create a new prediction record.
    
    No foreign key constraints - employee_number is stored as a simple integer.
    """
    try:
        prediction_data = prediction.model_dump()
        
        # Ensure prediction_date is set
        if not prediction_data.get("prediction_date"):
            prediction_data["prediction_date"] = datetime.utcnow()
        
        created_prediction = crud.create_prediction(mongo_db, prediction_data)
        
        if not created_prediction:
            raise HTTPException(status_code=500, detail="Failed to create prediction")
        
        return created_prediction
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating prediction: {str(e)}")


@router.get("/", response_model=list[Prediction])
def get_predictions(
    skip: int = Query(0, description="Number of records to skip for pagination"),
    limit: int = Query(10, description="Number of records to return"),
    employee_number: Optional[int] = Query(None, description="Filter by employee number")
):
    """
    Get predictions with optional filtering by employee number.
    """
    filters = {}
    if employee_number is not None:
        filters["employee_number"] = employee_number
    
    predictions = crud.get_predictions(mongo_db, skip=skip, limit=limit, filters=filters)
    return predictions


@router.get("/{prediction_id}", response_model=Prediction)
def get_prediction(prediction_id: str):
    """
    Get a specific prediction by ID.
    """
    prediction = crud.get_prediction(mongo_db, prediction_id)
    
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    return prediction


@router.get("/employee/{employee_number}", response_model=list[Prediction])
def get_predictions_by_employee(
    employee_number: int,
    limit: int = Query(10, description="Number of records to return")
):
    """
    Get all predictions for a specific employee number.
    """
    predictions = crud.get_predictions_by_employee(mongo_db, employee_number, limit=limit)
    return predictions

