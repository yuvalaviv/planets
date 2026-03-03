from pydantic import BaseModel
from datetime import datetime


class EntityModel(BaseModel):
    _id: str
    planet_id: str
    created_at: datetime | None = None
    type: str