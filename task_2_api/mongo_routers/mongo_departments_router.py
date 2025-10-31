from fastapi import APIRouter, HTTPException
from .. import schemas
from ..mongodb_crud import departments_crud as crud

router = APIRouter(
    prefix="/mongo",
    tags=["Departments"]
)

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
