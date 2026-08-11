Heroes Chess — Phase 0 Dev Setup

Backend (PowerShell)

```powershell
# create venv and activate
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend/requirements.txt

# create db
python backend/scripts/create_db.py

# run backend (from project root)
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

Frontend

```powershell
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm install @apollo/client graphql react-router-dom react-chessboard
npm run dev
```

Notes
- This scaffold uses SQLite (`sqlite:///./dev.db`) for local development. Switch `DATABASE_URL` in `.env` to Postgres when ready.
- Alembic is intentionally skipped for rapid dev; add it before preserving production data.
