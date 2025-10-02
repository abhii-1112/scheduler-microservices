# app/scheduler.py
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime
from .database import SessionLocal
from .models import Job
from datetime import datetime
from urllib.parse import quote_plus
import os


password = quote_plus(os.getenv("DATABASE_PASSWORD"))
DB_URL = f"postgresql+psycopg2://postgres:{password}@localhost:5432/postgres"

jobstores = {
    "default": SQLAlchemyJobStore(url=DB_URL)
}

scheduler = BackgroundScheduler(jobstores=jobstores)

def dummy_task(job_id: int):
    print(f"🕒 Running job {job_id} at {datetime.now()}")

def trigger_job(job_id: int):
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return

        # mark running
        job.status = "running"
        db.commit()

        # Dummy work: just update last_run and status success
        now = datetime.utcnow()
        job.last_run = now
        job.status = "success"
        db.commit()
    finally:
        db.close()

def add_job(job_id: int, schedule: str):
    if schedule.startswith("interval:"):
        seconds = int(schedule.split(":")[1])
        job = scheduler.add_job(
            dummy_task,
            trigger="interval",
            seconds=seconds,
            args=[job_id],
            id=str(job_id),
            replace_existing=True
        )
    elif schedule.startswith("cron:"):
        cron_expr = schedule.split(":")[1]
        job = scheduler.add_job(
            dummy_task,
            trigger="cron",
            args=[job_id],
            id=str(job_id),
            replace_existing=True,
            **_parse_cron(cron_expr)
        )
    print(f"✅ Job {job_id} scheduled with {schedule}")
    return job


def _parse_cron(expr: str):
    # quick parser for "0 9 * * 1"
    minute, hour, day, month, day_of_week = expr.split()
    return {
        "minute": minute,
        "hour": hour,
        "day": day,
        "month": month,
        "day_of_week": day_of_week
    }

def job_listener(event):
    db = SessionLocal()
    try:
        # event.job_id is string
        try:
            jid_int = int(event.job_id)
        except Exception:
            jid_int = None

        if jid_int is None:
            return

        db_job = db.query(Job).filter(Job.id == jid_int).first()
        if not db_job:
            return

        if event.exception:
            db_job.status = "failed"
        else:

            db_job.status = "scheduled"


        sched_job = scheduler.get_job(str(jid_int))
        if sched_job and sched_job.next_run_time:
            db_job.next_run = sched_job.next_run_time

        db.commit()
    finally:
        db.close()

def start_scheduler():
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()
