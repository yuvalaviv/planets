from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
from datetime import datetime
from app.models.planet import PlanetModel


class PlanetMongoAccessor:
    def __init__(self, connection_string: str, database_name: str):
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db["planets"]

    async def get_all(self) -> List[PlanetModel]:
        cursor = self.collection.find({})
        planets = []
        async for doc in cursor:
            planets.append(PlanetModel(**doc))
        return planets

    async def get_by_id(self, id: str) -> Optional[PlanetModel]:
        doc = await self.collection.find_one({"_id": id})
        if doc:
            return PlanetModel(**doc)
        return None

    async def create(self, planet: PlanetModel):
        await self.collection.insert_one(planet.dict(by_alias=True))

    async def delete(self, id: str):
        await self.collection.delete_one({"_id": id})