from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from .. import models, schemas


def get_job_details(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.JobDetail).offset(skip).limit(limit).all()

def get_job_detail(db: Session, job_id: int):
    job = db.query(models.JobDetail).filter(models.JobDetail.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job detail not found")
    return job

def create_job_detail(db: Session, job_detail: schemas.JobDetailCreate):
    db_job = models.JobDetail(**job_detail.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def update_job_detail(db: Session, job_id: int, job_detail: schemas.JobDetailCreate):
    db_job = get_job_detail(db, job_id)
    for key, value in job_detail.dict().items():
        setattr(db_job, key, value)
    db.commit()
    db.refresh(db_job)
    return db_job

def delete_job_detail(db: Session, job_id: int):
    db_job = get_job_detail(db, job_id)
    db.delete(db_job)
    db.commit()
    return {"message": f"Job detail {job_id} deleted successfully"}
