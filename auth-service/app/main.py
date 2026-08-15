from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import sql_health
from app.routes import auth

app = FastAPI(
    title="Authentication-Authorization-Service",
    description="Stack: FastAPI + PostgreSQL + SQLAlchemy + JWT (python-jose) + passlib + Authlib (Google OAuth) + slowapi (rate limiting) Frontend: React + MUI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://authentication-authorization-servic.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome to the Authenticatopn Project!"}

app.include_router(sql_health.router)
app.include_router(auth.router)