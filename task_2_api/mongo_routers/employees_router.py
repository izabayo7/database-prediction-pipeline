from fastapi import APIRouter, HTTPException
from .. import schemas
from ..crud import mongo_crud as crud

router = APIRouter(
    prefix="/mongo",
    tags=["MongoDB APIs"]
)

# ================= EMPLOYEES =================
@router.get("/employees", response_model=list[schemas.Employee])
def list_employees(skip: int = 0, limit: int = 10):
    return crud.get_employees(skip, limit)

@router.get("/employees/{id}", response_model=schemas.Employee)
def get_employee(id: str):
    emp = crud.get_employee(id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.post("/employees", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate):
    return crud.create_employee(employee.dict())

@router.put("/employees/{id}", response_model=schemas.Employee)
def update_employee(id: str, employee: schemas.EmployeeCreate):
    emp = crud.update_employee(id, employee.dict())
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.delete("/employees/{id}")
def delete_employee(id: str):
    success = crud.delete_employee(id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}


# ================= DEPARTMENTS =================
@router.get("/departments", response_model=list[schemas.Department])
def list_departments(skip: int = 0, limit: int = 10):
    return crud.get_departments(skip, limit)

@router.get("/departments/{id}", response_model=schemas.Department)
def get_department(id: str):
    dept = crud.get_department(id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

@router.post("/departments", response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate):
    return crud.create_department(department.dict())

@router.put("/departments/{id}", response_model=schemas.Department)
def update_department(id: str, department: schemas.DepartmentCreate):
    dept = crud.update_department(id, department.dict())
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

@router.delete("/departments/{id}")
def delete_department(id: str):
    success = crud.delete_department(id)
    if not success:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"message": "Department deleted successfully"}


# ================= JOB DETAILS =================
@router.get("/job_details", response_model=list[schemas.JobDetail])
def list_job_details(skip: int = 0, limit: int = 10):
    return crud.get_job_details(skip, limit)

@router.get("/job_details/{id}", response_model=schemas.JobDetail)
def get_job_detail(id: str):
    detail = crud.get_job_detail(id)
    if not detail:
        raise HTTPException(status_code=404, detail="Job Detail not found")
    return detail

@router.post("/job_details", response_model=schemas.JobDetail)
def create_job_detail(detail: schemas.JobDetailCreate):
    return crud.create_job_detail(detail.dict())

@router.put("/job_details/{id}", response_model=schemas.JobDetail)
def update_job_detail(id: str, detail: schemas.JobDetailCreate):
    updated = crud.update_job_detail(id, detail.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Job Detail not found")
    return updated

@router.delete("/job_details/{id}")
def delete_job_detail(id: str):
    success = crud.delete_job_detail(id)
    if not success:
        raise HTTPException(status_code=404, detail="Job Detail not found")
    return {"message": "Job Detail deleted successfully"}