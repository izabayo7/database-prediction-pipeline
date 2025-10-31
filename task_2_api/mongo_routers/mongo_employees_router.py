from fastapi import APIRouter, HTTPException
from .. import schemas
from ..mongodb_crud import employees_crud as crud

router = APIRouter(
    prefix="/mongo",
    tags=["Employees"]
)

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

