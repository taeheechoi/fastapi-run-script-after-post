import os
from datetime import datetime
from glob import glob
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, validator
import uvicorn

from gmail import email_with_attachment

app = FastAPI()

class DateTimeModeMixin(BaseModel):
    # To add timestamp script executed, https://pydantic-docs.helpmanual.io/usage/validators/
    created_at: datetime = None

    @validator("created_at", pre=True, always=True)
    def default_datetime(cls, value:datetime) -> datetime:
        return value or datetime.now()

class Job(DateTimeModeMixin):
    name: str
    description: Optional[str]

jobs = []

def job_email_with_attachment():
    to_email = os.getenv("TO_EMAIL").split(';')
    attachments = glob('data/*.csv')
    email_with_attachment(header='header...', recipient=to_email, body='body...', attachments=attachments)

@app.get('/jobs')
async def get_jobs():
    return jobs

@app.post('/jobs', status_code=201)
async def add_job(job: Job):
    jobs.append(job)
    job_email_with_attachment()
    return jobs

if __name__ == '__main__':
    uvicorn.run(app)
