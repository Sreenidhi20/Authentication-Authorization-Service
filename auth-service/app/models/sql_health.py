from database import Base
from sqlalchemy import Column, Integer, String


class HealthCheck(Base):
    __tablename__ = "HealthCheck"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(5))
    message = Column(String(20))