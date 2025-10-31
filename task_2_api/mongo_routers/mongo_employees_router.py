from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from task_2_api import schemas
from ..mongo_database import mongo_db
from ..mongodb_crud import employees_crud as crud
from ..mongodb_schemas import Employee, EmployeeBase

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


@router.post("/", response_model=Employee) 
def create_employee(employee: EmployeeBase):
    return crud.create_employee(mongo_db, employee.dict())


@router.put("/{employee_id}", response_model=Employee)
def update_employee(employee_id: str, employee: EmployeeBase):
    updated = crud.update_employee(mongo_db, employee_id, employee.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated

@router.delete("/{employee_id}")
def delete_employee(employee_id: str):
    return crud.delete_employee(mongo_db, employee_id)
