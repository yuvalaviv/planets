# app/domain/entities/base_entity.py
from pydantic import BaseModel, Field
from datetime import datetime


class EntityBase(BaseModel):
    """
    Domain model representing an entity.
    """
    ID: str = Field(alias="_id")
    planet_id: str
    created_at: datetime
    type: str

    class Config:
        populate_by_name = True
