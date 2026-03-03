from datetime import datetime
from pydantic import BaseModel

class PlanetModel(BaseModel):
    _id: str
    name: str
    created_at: datetime