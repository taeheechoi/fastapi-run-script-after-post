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
    created_at: datetime = None

    @validator("created_at", pre=True, always=True)
    def default_datetime(cls, value:datetime) -> datetime:
        return value or datetime.now()

class Log(DateTimeModeMixin):
    name: str
    description: Optional[str]

logs = []

def run_script():
    to_email = os.getenv("TO_EMAIL").split(';')
    attachments = glob('data/*.csv')
    email_with_attachment(header='header...', recipient=to_email, body='body...', attachments=attachments)

@app.get('/logs')
async def get_logs():
    return logs

@app.post('/logs', status_code=201)
async def add_log(log: Log):
    logs.append(log)
    run_script()
    return logs

if __name__ == '__main__':
    uvicorn.run(app)
