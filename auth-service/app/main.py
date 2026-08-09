from fastapi import FastAPI

from app.routes import sql_health

app = FastAPI(
    title="Authentication-Authorization-Service",
    description="Stack: FastAPI + PostgreSQL + SQLAlchemy + JWT (python-jose) + passlib + Authlib (Google OAuth) + slowapi (rate limiting) Frontend: React + MUI",
    version="1.0.0",
)

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome to the Authenticatopn Project!"}

app.include_router(sql_health.router)