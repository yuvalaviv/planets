from datetime import datetime
from pydantic import BaseModel, Field


class PlanetModel(BaseModel):
    ID: str = Field(alias="_id")
    name: str
    created_at: datetime
