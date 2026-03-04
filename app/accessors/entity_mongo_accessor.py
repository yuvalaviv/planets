from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel
from app.config import settings
from pymongo.errors import DuplicateKeyError

from app.models.animal import Animal
from app.models.base_entity import EntityBase
from app.schema.entity_schema import EntityResponse


class EntityMongoAccessor:
    """
    Data access layer for Entity documents stored in MongoDB.

    This class encapsulates all CRUD operations related to entities
    and provides an asynchronous interface using Motor.

    Attributes:
        collection: MongoDB collection instance used for entity storage.
    """
    def __init__(self, db: AsyncIOMotorDatabase):
        """
        Initialize the accessor with a MongoDB database instance.

        Args:
            db: AsyncIOMotorDatabase instance connected to MongoDB.
        """
        self.collection = db[settings.ENTITIES_DB]

    async def create(self, entity: BaseModel) -> str:
        """
        Insert a new entity document into MongoDB.

        Args:
            entity: Pydantic model representing the entity.

        Returns:
            The inserted entity ID as a string.
        """
        try:
            doc = entity.model_dump(by_alias=True)
            result = await self.collection.insert_one(doc)
            return str(result.inserted_id)

        except DuplicateKeyError:
            raise ValueError("Entity with id %s already exists" % entity.ID)

    async def get_by_id(self, entity_id: str) -> Optional[BaseModel]:
        """
        Retrieve an entity document by its ID.

        Args:
            entity_id: The unique identifier of the entity.

        Returns:
            The entity document as a dictionary if found,
            otherwise None.
        """
        return await self.collection.find_one({"_id": entity_id})

    async def get_all(self) -> List[dict]:
        """
        Retrieve all entity documents from the collection.

        Returns:
            A list of entity documents as dictionaries.
        """
        cursor = self.collection.find({})
        return [doc async for doc in cursor]

    async def delete(self, entity_id: str) -> bool:
        """
        Delete an entity by its ID.

        Args:
            entity_id: The unique identifier of the entity.

        Returns:
            True if the entity was deleted, False otherwise.
        """
        result = await self.collection.delete_one({"_id": entity_id})
        return result.deleted_count > 0

    async def update_fields(self, entity_id: str, fields: Dict[str, Any]) -> bool:
        """
        Update specific fields of an entity document.

        Args:
            entity_id: The unique identifier of the entity.
            fields: Dictionary of fields to update.

        Returns:
            True if the entity was updated, False otherwise.
        """
        result = await self.collection.update_one(
            {"_id": entity_id},
            {"$set": fields}
        )
        return result.modified_count > 0
