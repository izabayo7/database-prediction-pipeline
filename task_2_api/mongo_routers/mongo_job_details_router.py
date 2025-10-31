from fastapi import APIRouter, HTTPException
from .. import schemas
from ..mongodb_crud import job_details_crud as crud

router = APIRouter(
    prefix="/mongo",
    tags=["Mongo Job Details"]
)

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