# app/accessors/entity_accessor.py
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel


class EntityMongoAccessor:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["entities"]

    async def create(self, entity: BaseModel) -> str:
        """
        entity: Pydantic model (Tree or Animal)
        """
        doc = entity.dict(by_alias=True)
        result = await self.collection.insert_one(doc)
        return str(result.inserted_id)

    async def get_by_id(self, entity_id: str) -> Optional[dict]:
        doc = await self.collection.find_one({"_id": entity_id})
        return doc

    async def get_all(self) -> List[dict]:
        cursor = self.collection.find({})
        return [doc async for doc in cursor]

    async def delete(self, entity_id: str) -> bool:
        result = await self.collection.delete_one({"_id": entity_id})
        return result.deleted_count > 0

    async def update_fields(self, entity_id: str, fields: dict):
        await self.collection.update_one(
            {"_id": entity_id},
            {"$set": fields}
        )
