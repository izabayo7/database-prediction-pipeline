from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..mysql_crud import employees_crud as crud
from .. import models, schemas


router = APIRouter(
    prefix="/mysql/employees",
    tags=["Employees (MYSQL)"] 
)

@router.get("/", response_model=list[schemas.Employee])
def list_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_employees(db, skip, limit)

@router.post("/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)

@router.get("/{employee_number}", response_model=schemas.Employee)
def get_employee(employee_number: int, db: Session = Depends(get_db)):
    emp = crud.get_employee(db, employee_number)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.put("/{employee_number}", response_model=schemas.Employee)
def update_employee(employee_number: int, employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.update_employee(db, employee_number, employee)

@router.delete("/{employee_number}")
def delete_employee(employee_number: int, db: Session = Depends(get_db)):
    return crud.delete_employee(db, employee_number)



