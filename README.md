# Job Scheduler Microservice

A FastAPI-based microservice for scheduling and managing jobs with flexible intervals or cron expressions.  
This service includes API endpoints to create, list, and retrieve jobs, while persisting job metadata in PostgreSQL.

---

## **Features**

- **Job Scheduling**
  - Supports cron-based and interval-based jobs.
  - Tracks last run, next run, and job status.
  - Dummy job execution included for POC (can be replaced with real tasks).

- **API Endpoints**
  - `POST /api/jobs` – Create a new job
  - `GET /api/jobs` – List all jobs
  - `GET /api/jobs/{id}` – Get details of a specific job

- **Database Integration**
  - Stores job name, schedule, payload, last/next run timestamps, status, description.
  - PostgreSQL used with SQLAlchemy ORM.
  
- **Scalable**
  - BackgroundScheduler (APScheduler) used to handle multiple jobs efficiently.

---

## **Tech Stack**

- Python 3.11+  
- FastAPI  
- SQLAlchemy  
- PostgreSQL  
- APScheduler  

---

## **Setup**

1. **Clone the repository**

```bash
git clone https://github.com/username/job-scheduler-microservice.git
cd job-scheduler-microservice
