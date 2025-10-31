from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from ..mysql_crud import mysql_departments_crud as crud

router = APIRouter(
    prefix="/mysql/departments",
    tags=["Departments"]
)

@router.get("/", response_model=list[schemas.Department])
def list_departments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_departments(db, skip, limit)

@router.post("/", response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db, department)

@router.put("/{department_id}", response_model=schemas.Department)
def update_department(department_id: int, department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.update_department(db, department_id, department)

@router.delete("/{department_id}")
def delete_department(department_id: int, db: Session = Depends(get_db)):
    return crud.delete_department(db, department_id)



