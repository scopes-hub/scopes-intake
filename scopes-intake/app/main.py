from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import init_db
from app.routes.leads import router as leads_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Lead Intake API", version="0.1.0", lifespan=lifespan)
app.include_router(leads_router)
