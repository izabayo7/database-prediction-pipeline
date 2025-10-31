from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from .. import models, schemas

#Department CRUD Operations

def get_departments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Department).offset(skip).limit(limit).all()

def get_department(db: Session, department_id: int):
    dept = db.query(models.Department).filter(models.Department.department_id == department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

def create_department(db: Session, department: schemas.DepartmentCreate):
    db_dept = models.Department(**department.dict())
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept

def update_department(db: Session, department_id: int, department: schemas.DepartmentCreate):
    db_dept = get_department(db, department_id)
    db_dept.department_name = department.department_name
    db.commit()
    db.refresh(db_dept)
    return db_dept

def delete_department(db: Session, department_id: int):
    db_dept = get_department(db, department_id)
    db.delete(db_dept)
    db.commit()
    return {"message": f"Department {department_id} deleted successfully"}