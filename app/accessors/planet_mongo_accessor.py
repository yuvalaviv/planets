from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel
from app.config import settings
from pymongo.errors import DuplicateKeyError


class PlanetMongoAccessor:
    """
    Data access layer for Planet documents stored in MongoDB.

    This class encapsulates all CRUD operations related to planets
    and provides an asynchronous interface using Motor.

    Attributes:
        collection: MongoDB collection instance used for planet storage.
    """
    def __init__(self, db: AsyncIOMotorDatabase):
        """
        Initialize the accessor with a MongoDB database instance.

        Args:
            db: AsyncIOMotorDatabase instance connected to MongoDB.
        """
        self.collection = db[settings.PLANETS_DB]

    async def create(self, planet: BaseModel) -> str:
        """
        Insert a new planet document into MongoDB.

        Args:
            planet: Pydantic model representing the planet.

        Returns:
            The inserted planet ID as a string.
        """
        try:
            doc = planet.model_dump(by_alias=True)
            result = await self.collection.insert_one(doc)
            return str(result.inserted_id)

        except DuplicateKeyError:
            raise ValueError(settings.DUPLICATE_PLANET_ERROR % planet.ID)

    async def get_by_id(self, planet_id: str) -> Optional[BaseModel]:
        """
        Retrieve a planet document by its ID.

        Args:
            planet_id: The unique identifier of the planet.

        Returns:
            The planet document as a dictionary if found,
            otherwise None.
        """
        doc = await self.collection.find_one({"_id": planet_id})
        return doc

    async def get_all(self) -> List[dict]:
        """
        Retrieve all planet documents from the collection.

        Returns:
            A list of planet documents as dictionaries.
        """
        cursor = self.collection.find({})
        return [doc async for doc in cursor]

    async def delete(self, planet_id: str) -> bool:
        """
        Delete an planet by its ID.

        Args:
            planet_id: The unique identifier of the planet.

        Returns:
            True if the planet was deleted, False otherwise.
        """
        result = await self.collection.delete_one({"_id": planet_id})
        return result.deleted_count > 0
