from datetime import datetime
from pydantic import BaseModel, Field


class PlanetModel(BaseModel):
    """
    Domain model representing a Planet
    """
    ID: str = Field(alias="_id")
    name: str
    created_at: datetime
