from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
from app.models.entity import Entity


class EntityMongoAccessor:
    def __init__(self, connection_string: str, database_name: str):
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db["entities"]

    async def get_all(self) -> List[Entity]:
        """Return all entities as EntityModel objects"""
        cursor = self.collection.find({})
        entities = []
        async for doc in cursor:
            entities.append(Entity.from_dict(**doc))
        return entities

    async def get_by_id(self, entity_id: str) -> Optional[dict]:
        return await self.collection.find_one({"_id": entity_id})

    async def create(self, entity: Entity):
        await self.collection.insert_one(entity.dict(by_alias=True))

    async def delete(self, id: str):
        await self.collection.delete_one({"_id": id})
