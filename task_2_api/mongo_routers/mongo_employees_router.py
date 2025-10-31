from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..mongo_database import mongo_db
from ..mongodb_crud import employees_crud as crud

router = APIRouter(
    prefix="/mongo/employees",
    tags=["MongoDB Employees"]
)

@router.get("/")
def get_employees(
    skip: int = Query(0, description="Number of records to skip for pagination"),
    limit: int = Query(10, description="Number of records to return"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    attrition: Optional[str] = Query(None, description="Filter by attrition"),
    education_field: Optional[str] = Query(None, description="Filter by education field"),
):
    # Build filter dictionary dynamically
    filters = {}
    if gender:
        filters["gender"] = gender
    if attrition:
        filters["attrition"] = attrition
    if education_field:
        filters["education_field"] = education_field

    employees = crud.get_employees(mongo_db, skip=skip, limit=limit, filters=filters)
    return employees


@router.get("/{employee_id}")
def get_employee(employee_id: str):
    emp = crud.get_employee(mongo_db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.post("/")
def create_employee(employee: dict):
    return crud.create_employee(mongo_db, employee)


@router.put("/{employee_id}")
def update_employee(employee_id: str, employee: dict):
    updated = crud.update_employee(mongo_db, employee_id, employee)
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated


@router.delete("/{employee_id}")
def delete_employee(employee_id: str):
    return crud.delete_employee(mongo_db, employee_id)
