from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LeadCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    company: str = Field(..., min_length=1, max_length=200)
    industry: str = Field(..., min_length=1, max_length=100)
    company_size: str = Field(..., min_length=1, max_length=50)
    region: str = Field(..., min_length=1, max_length=50)


class LeadStatusUpdate(BaseModel):
    status: Literal["new", "contacted", "closed"]


class LeadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    status: Literal["new", "contacted", "closed"]
    name: str
    email: EmailStr
    company: str
    industry: str
    company_size: str
    region: str
    score: int
    route: str
    idempotency_key: str
