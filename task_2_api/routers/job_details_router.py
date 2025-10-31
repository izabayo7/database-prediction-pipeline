from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import mysql_ob_details_crud as crud
from .. import schemas

router = APIRouter(
    prefix="/job_details",
    tags=["Job Details"]
)

@router.get("/", response_model=list[schemas.JobDetail])
def list_job_details(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_job_details(db, skip, limit)

@router.post("/", response_model=schemas.JobDetail)
def create_job_detail(job_detail: schemas.JobDetailCreate, db: Session = Depends(get_db)):
    return crud.create_job_detail(db, job_detail)

@router.put("/{job_id}", response_model=schemas.JobDetail)
def update_job_detail(job_id: int, job_detail: schemas.JobDetailCreate, db: Session = Depends(get_db)):
    return crud.update_job_detail(db, job_id, job_detail)

@router.delete("/{job_id}")
def delete_job_detail(job_id: int, db: Session = Depends(get_db)):
    return crud.delete_job_detail(db, job_id)
