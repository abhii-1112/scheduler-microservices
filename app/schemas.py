
from pydantic import BaseModel, Field, validator, field_validator
from typing import Optional, Dict, Any
from datetime import datetime
import re

CRON_5_PARTS = re.compile(r'^\s*([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s*$')

class JobBase(BaseModel):
    name: str = Field(..., max_length=150)
    schedule: str = Field(..., description="Cron expression with 5 fields (min hour day month weekday)")
    payload: Optional[Dict[str, Any]] = None
    description: Optional[str] = None

    @field_validator("schedule")
    def validate_schedule(cls, v):
        if v.startswith("interval:"):
            if not v.split(":")[1].isdigit():
                raise ValueError("Interval must be an integer number of seconds")
            return v
        elif CRON_5_PARTS.match(v):
            return v
        else:
            raise ValueError("Invalid schedule. Use 'interval:<seconds>' or 5-field cron expression")


class JobCreate(JobBase):
    pass

class JobRead(JobBase):
    id: int
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        form_attributes = True
