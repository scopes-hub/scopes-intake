from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models
from app.db import get_session
from app.schemas import LeadCreate, LeadOut, LeadStatusUpdate
from app.scoring import load_rules, score_lead

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/leads", response_model=LeadOut, status_code=201)
def create_lead(
    payload: LeadCreate,
    response: Response,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    session: Session = Depends(get_session),
):
    existing = session.execute(
        select(models.Lead).where(models.Lead.idempotency_key == idempotency_key)
    ).scalar_one_or_none()
    if existing:
        response.status_code = 200
        return existing

    rules = load_rules()
    score, route = score_lead(payload.model_dump(), rules)

    lead = models.Lead(
        name=payload.name,
        email=payload.email,
        company=payload.company,
        industry=payload.industry,
        company_size=payload.company_size,
        region=payload.region,
        score=score,
        route=route,
        idempotency_key=idempotency_key,
    )
    session.add(lead)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        existing = session.execute(
            select(models.Lead).where(models.Lead.idempotency_key == idempotency_key)
        ).scalar_one_or_none()
        if existing:
            response.status_code = 200
            return existing
        raise
    session.refresh(lead)
    return lead


@router.get("/leads", response_model=list[LeadOut])
def list_leads(status: Optional[str] = None, session: Session = Depends(get_session)):
    query = select(models.Lead).order_by(models.Lead.created_at.desc())
    if status:
        query = query.where(models.Lead.status == status)
    return session.execute(query).scalars().all()


@router.patch("/leads/{lead_id}/status", response_model=LeadOut)
def update_status(
    lead_id: int, payload: LeadStatusUpdate, session: Session = Depends(get_session)
):
    lead = session.get(models.Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead.status = payload.status
    session.commit()
    session.refresh(lead)
    return lead


@router.get("/admin/leads", response_class=HTMLResponse)
def admin_leads(
    request: Request, status: Optional[str] = None, session: Session = Depends(get_session)
):
    query = select(models.Lead).order_by(models.Lead.created_at.desc())
    if status:
        query = query.where(models.Lead.status == status)
    leads = session.execute(query).scalars().all()
    return templates.TemplateResponse(
        "admin.html", {"request": request, "leads": leads, "status": status or ""}
    )
