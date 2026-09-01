# Cloud-Based Fleet Fuel Consumption Analytics

A full-stack demo project for tracking a vehicle fleet's fuel consumption and
viewing analytics (total fuel used, cost, monthly trends, per-vehicle
average consumption).

## Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-CORS
- **Database:** SQLite by default (file-based, zero setup). `DATABASE_URL`
  can be swapped for PostgreSQL/MySQL for a "cloud" deployment.
- **Frontend:** Static HTML/CSS/JavaScript + Chart.js (no build step required)
- **Containerization:** Docker + docker-compose (optional, for the backend)

## Project Structure

```
fleet-fuel-analytics/
├── backend/
│   ├── app.py            # Flask app factory / entry point
│   ├── database.py       # SQLAlchemy db instance
│   ├── models.py         # Vehicle, FuelLog models
│   ├── routes.py         # REST API endpoints (/api/...)
│   ├── seed_data.py      # Populates sample vehicles + fuel logs
│   ├── requirements.txt  # Python dependencies
│   ├── .env.example      # Example environment variables
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
├── docker-compose.yml
└── README.md
```

## API Endpoints

| Method | Endpoint                        | Description                        |
|--------|----------------------------------|-------------------------------------|
| GET    | `/api/vehicles`                 | List all vehicles                   |
| POST   | `/api/vehicles`                 | Add a vehicle                       |
| GET    | `/api/fuel-logs`                | List fuel logs (optional `?vehicle_id=`) |
| POST   | `/api/fuel-logs`                | Add a fuel log entry                |
| GET    | `/api/analytics/summary`        | Fleet-wide totals                   |
| GET    | `/api/analytics/monthly`        | Monthly fuel/cost trend             |
| GET    | `/api/analytics/vehicle/<id>`   | Per-vehicle average consumption     |

## Quick Start (local, no Docker)

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env
python seed_data.py
python app.py
```

Then open `frontend/index.html` in your browser (or serve it with
`npx serve frontend`), with the backend running at `http://localhost:5000`.

## Quick Start (Docker, backend only)

```bash
docker-compose up --build
```

Frontend is still opened as a static file / served separately — see the
setup guide for full details.
