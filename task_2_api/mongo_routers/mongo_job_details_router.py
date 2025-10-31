from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from .. import mongodb_schemas as schemas
from ..mongodb_crud import job_details_crud as crud

router = APIRouter(
    prefix="/mongo/job_details",
    tags=["Job Details (MongoDB)"]
)

@router.post("/", response_model=schemas.JobDetail)
def create_job_detail(job_detail: schemas.JobDetailCreate):
    return crud.create_job_detail(job_detail.model_dump())

@router.get("/", response_model=List[schemas.JobDetail])
def list_job_details(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    return crud.get_job_details(skip=skip, limit=limit)

@router.get("/{job_id}", response_model=schemas.JobDetail)
def get_job_detail(job_id: str):
    job = crud.get_job_detail(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job detail not found")
    return job

@router.put("/{job_id}", response_model=schemas.JobDetail)
def update_job_detail(job_id: str, job_detail: schemas.JobDetailCreate):
    updated = crud.update_job_detail(job_id, job_detail.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Job detail not found or not updated")
    return updated

@router.delete("/{job_id}")
def delete_job_detail(job_id: str):
    deleted = crud.delete_job_detail(job_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Job detail not found or already deleted")
    return {"message": f"Job detail {job_id} deleted successfully"}
