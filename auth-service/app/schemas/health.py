from pydantic import BaseModel

class HealthCheckResponse(BaseModel):
    """Schema for the health check response."""

    status: str
    message: str