from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db 

router = APIRouter(
    prefix="/health",
    tags=["Health Check"],
)

@router.get("")
def sql_health_check(db: Session = Depends(get_db)):
    try:
        # Executes raw SQL safely through the SQLAlchemy connection pool
        result = db.execute(text("SELECT status, message FROM HealthCheck;")).fetchone()
        
        if not result:
            return {
                "status": "UNKNOWN",
                "message": "No rows returned from health check table"
            }
            
        # SQLAlchemy returns tuple-like rows, access elements by index or key
        return {
            "status": result[0],    # maps to status
            "message": result[1]    # maps to message
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)            
        }
