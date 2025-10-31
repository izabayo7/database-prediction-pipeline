from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from .. import mongodb_schemas as schemas
from ..mongodb_crud import departments_crud  as crud
from ..mongodb_schemas import Department as MongoDepartment

router = APIRouter(
    prefix="/mongo/departments",
    tags=["Departments (MongoDB)"]
)

@router.get("/", response_model=List[MongoDepartment])
def list_mongo_departments(skip: int = 0, limit: int = 10):
    docs = crud.get_departments(skip=skip, limit=limit)  # returns dicts with 'department_id' as str
    return docs

@router.get("/{id}", response_model=MongoDepartment)
def read_mongo_department(id: str):
    doc = crud.get_department(id)
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    return doc

@router.post("/", response_model=MongoDepartment)
def post_mongo_department(payload: dict):
    created = crud.create_department(payload)
    return created

@router.put("/{department_id}", response_model=MongoDepartment)
def update_department(department_id: str, department: MongoDepartment):
    updated = crud.update_department(department_id, department.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Department not found or not updated")
    return updated

@router.delete("/{department_id}")
def delete_department(department_id: str):
    deleted = crud.delete_department(department_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Department not found or already deleted")
    return {"message": f"Department {department_id} deleted successfully"}
