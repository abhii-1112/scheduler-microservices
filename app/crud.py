# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Job).order_by(models.Job.id.desc()).offset(skip).limit(limit).all()

def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(
        name=job.name,
        schedule=job.schedule,   # consistent field name
        payload=job.payload,
        description=job.description,
        last_run=None,
        next_run=None,
        status="scheduled"
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def update_job_next_run(db: Session, job_id: int, next_run):
    job = get_job(db, job_id)
    if job:
        job.next_run = next_run
        db.commit()
        db.refresh(job)
    return job

def update_job_status_and_last_run(db: Session, job_id: int, status: str, last_run):
    job = get_job(db, job_id)
    if job:
        job.status = status
        job.last_run = last_run
        db.commit()
        db.refresh(job)
    return job
