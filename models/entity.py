from pydantic import BaseModel
from datetime import datetime


class EntityModel(BaseModel):
    ID: str
    planet_id: str
    created_at: datetime | None = None
    type: str