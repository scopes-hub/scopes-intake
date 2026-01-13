from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI, Request

from app import models
from app.db import SessionLocal, init_db
from app.routes.leads import router as leads_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


#log requests
app = FastAPI(title="Lead Intake API", version="0.1.0", lifespan=lifespan)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = perf_counter()
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        duration_ms = int((perf_counter() - start) * 1000)
        client_ip = request.client.host if request.client else ""
        user_agent = request.headers.get("user-agent", "")
        query_params = request.url.query[:1000]
        try:
            with SessionLocal() as session:
                entry = models.ApiRequestLog(
                    method=request.method,
                    path=request.url.path,
                    query_params=query_params,
                    status_code=status_code,
                    duration_ms=duration_ms,
                    client_ip=client_ip,
                    user_agent=user_agent[:300],
                )
                session.add(entry)
                session.commit()
        except Exception:
            pass


app.include_router(leads_router)
