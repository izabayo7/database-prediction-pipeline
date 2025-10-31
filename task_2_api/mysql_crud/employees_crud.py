from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas

def get_employees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Employee).offset(skip).limit(limit).all()

def get_employee(db: Session, employee_number: int):
    return db.query(models.Employee).filter(models.Employee.employee_number == employee_number).first()

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_emp = models.Employee(**employee.dict(exclude={"department_name", "job_satisfaction", "job_involvement"}))
    db.add(db_emp)
    db.flush() 

    dept_name = getattr(employee, "department_name", None)
    job_satisfaction = getattr(employee, "job_satisfaction", None)
    job_involvement = getattr(employee, "job_involvement", None)

    if dept_name:
        dept = db.query(models.Department).filter_by(department_name=dept_name).first()
        if not dept:
            dept = models.Department(department_name=dept_name)
            db.add(dept)
            db.flush()
    else:
        dept = db.query(models.Department).filter_by(department_name="General").first()
        if not dept:
            dept = models.Department(department_name="General")
            db.add(dept)
            db.flush()
    
    job_detail = models.JobDetail(
        employee_number=db_emp.employee_number,
        department_id=dept.department_id,
        job_role="Developer",
        job_level=2,
        job_satisfaction=job_satisfaction or 3,
        job_involvement=job_involvement or 3,
    )
    db.add(job_detail)

    db.commit()
    db.refresh(db_emp)
    return db_emp

def update_employee(db: Session, employee_number: int, employee: schemas.EmployeeCreate):
    db_emp = get_employee(db, employee_number)
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    # update department if provided
    if employee.department_name:
        dept = db.query(models.Department).filter_by(department_name=employee.department_name).first()
        if not dept:
            dept = models.Department(department_name=employee.department_name)
            db.add(dept)
            db.flush()

        job_detail = db.query(models.JobDetail).filter_by(employee_number=employee_number).first()
        if job_detail:
            job_detail.department_id = dept.department_id

    # update other fields
    for key, value in employee.dict(exclude={"department_name"}).items():
        setattr(db_emp, key, value)

    db.commit()
    db.refresh(db_emp)
    return db_emp

def delete_employee(db: Session, employee_number: int):
    employee = db.query(models.Employee).filter(models.Employee.employee_number == employee_number).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    try:
        db.delete(employee)
        db.commit()
        return {"message": f"Employee {employee_number} deleted successfully"}
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Delete failed: {str(e)}")
    


