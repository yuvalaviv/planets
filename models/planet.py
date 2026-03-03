from datetime import datetime
from pydantic import BaseModel

class PlanetModel(BaseModel):
    id: str
    name: str
    created_at: datetime | None = None