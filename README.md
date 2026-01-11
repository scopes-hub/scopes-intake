# scopes-intake
scopes-intake is a small FastAPI service that accepts inbound leads, scores them with simple rules, routes them to Sales/Support/Partnerships, and provides a lightweight admin view.

## Features
- Lead intake via `POST /leads` with idempotency support
- Simple scoring rules (industry, company size, email domain, region)
- Routing to Sales, Support, or Partnerships
- Admin page to view leads and status
- SQLite by default, Postgres-ready via `DATABASE_URL`

## Stack
- Python + FastAPI
- SQLAlchemy (SQLite/Postgres)
- Jinja2 admin UI

## Project layout
- `launch.py`: app launcher (loads `.env` and runs Uvicorn)
- `app/main.py`: FastAPI app and startup
- `app/routes/leads.py`: API endpoints and admin view
- `app/scoring.py`: rule loading + scoring logic
- `config/scoring_rules.json`: hard-coded scoring rules
- `scripts/seed.py`: seed data script
- `postman/lead-intake.postman_collection.json`: Postman collection

## Quickstart (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python launch.py
```

Open the admin view at `http://127.0.0.1:8000/admin/leads`.

## Seed sample data
PowerShell:
```powershell
$env:PYTHONPATH = "."
.\.venv\Scripts\python scripts\seed.py
```

## API
- `POST /leads`
  - Required header: `Idempotency-Key`
- `GET /leads?status=new|contacted|closed`
- `PATCH /leads/{lead_id}/status`
- `GET /admin/leads`

Example request:
```bash
curl -X POST http://127.0.0.1:8000/leads \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: demo-1" \
  -d '{
    "name": "Jamie Park",
    "email": "jamie@acme.com",
    "company": "Acme Corp",
    "industry": "software",
    "company_size": "enterprise",
    "region": "na"
  }'
```

## Configuration
Set these in `.env` (see `.env.example`):
- `DATABASE_URL` (default: `sqlite:///./data/app.db`)
- `HOST` (default: `127.0.0.1`)
- `PORT` (default: `8000`)
- `RELOAD` (default: `true`)
- `SCORING_RULES_PATH` (default: `config/scoring_rules.json`)

## Scoring rules
Edit `config/scoring_rules.json` to adjust weights and routing thresholds.

## Postman
Import `postman/lead-intake.postman_collection.json` to try the endpoints quickly.
