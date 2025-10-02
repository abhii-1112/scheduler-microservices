# app/routes/jobs.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from ..scheduler import add_job, scheduler
from typing import List
from app.database import get_db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


router = APIRouter()

@router.get("/test-db")
def test_db_endpoint(db: Session = Depends(get_db)):
    result = db.execute("SELECT version();")
    return {"db_version": result.scalar()}


@router.post("/jobs", response_model=schemas.JobRead, status_code=status.HTTP_201_CREATED)
def create_job(job_in: schemas.JobCreate, db: Session = Depends(get_db)):
    try:
        # 1. create DB record
        db_job = crud.create_job(db, job_in)

        # 2. schedule in APScheduler
        aps_job = add_job(db_job.id, db_job.schedule)

        # 3. persist next_run if APScheduler returns it
        if aps_job and aps_job.next_run_time:
            crud.update_job_next_run(db, db_job.id, aps_job.next_run_time)

        return crud.get_job(db, db_job.id)

    except IntegrityError:
        # Job with this name already exists
        raise HTTPException(
            status_code=400,
            detail=f"Job with name '{job_in.name}' already exists."
        )
    except SQLAlchemyError as e:
        # Other DB errors
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

@router.get("/jobs", response_model=List[schemas.JobRead])
def list_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_jobs(db, skip=skip, limit=limit)

@router.get("/jobs/{job_id}", response_model=schemas.JobRead)
def read_job(job_id: int, db: Session = Depends(get_db)):
    job = crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


