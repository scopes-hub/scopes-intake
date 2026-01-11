import uuid

from app import models
from app.db import SessionLocal, init_db
from app.scoring import load_rules, score_lead

SAMPLE_LEADS = [
    {
        "name": "Taylor Reed",
        "email": "taylor@acme.com",
        "company": "Acme Corp",
        "industry": "software",
        "company_size": "mid-market",
        "region": "na",
    },
    {
        "name": "Alex Chen",
        "email": "alex@healthbridge.org",
        "company": "HealthBridge",
        "industry": "healthcare",
        "company_size": "enterprise",
        "region": "emea",
    },
    {
        "name": "Morgan Diaz",
        "email": "morgan@gmail.com",
        "company": "Bootstrap Labs",
        "industry": "education",
        "company_size": "startup",
        "region": "apac",
    },
]


def main() -> None:
    init_db()
    rules = load_rules()
    with SessionLocal() as session:
        for data in SAMPLE_LEADS:
            score, route = score_lead(data, rules)
            lead = models.Lead(
                name=data["name"],
                email=data["email"],
                company=data["company"],
                industry=data["industry"],
                company_size=data["company_size"],
                region=data["region"],
                score=score,
                route=route,
                idempotency_key=f"seed-{uuid.uuid4().hex}",
            )
            session.add(lead)
        session.commit()


if __name__ == "__main__":
    main()
