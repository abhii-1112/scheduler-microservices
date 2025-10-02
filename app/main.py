# app/main.py
from fastapi import FastAPI
from .routes import jobs
from .scheduler import start_scheduler
from .database import init_db
from dotenv import load_dotenv
load_dotenv()
app = FastAPI(title="Job Scheduler Microservice")


@app.on_event("startup")
def startup_event():
    init_db()
    start_scheduler()

app.include_router(jobs.router, prefix="/api")
