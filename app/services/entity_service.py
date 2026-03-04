from pymongo.errors import DuplicateKeyError

from app.accessors.entity_mongo_accessor import EntityMongoAccessor
from app.infrastructure.unix_socket.client import UnixSocketClient
from app.models.base_entity import EntityBase
from typing import List, Optional
from pydantic import parse_obj_as
from app.config import settings

from app.schema.entity_schema import EntityResponse


class EntityService:
    """
    Application service layer responsible for managing Entity operations.

    This service coordinates between:
        - The persistence layer (EntityMongoAccessor)
        - The event communication layer (UnixSocketClient)

    It ensures that entity lifecycle events (e.g., creation)
    are both persisted in the database and propagated
    to the socket-based processing system.
    """

    def __init__(self, accessor: EntityMongoAccessor, socket_client: UnixSocketClient):
        """
        Initialize the service with required dependencies.

        Args:
            accessor: Data access layer for entity persistence.
            socket_client: Unix domain socket used for inter-process communication.
        """
        self.accessor = accessor
        self.socket_client = socket_client

    async def get_all_entities(self) -> List[EntityResponse]:
        """
        Retrieve all entities from the database.

        Returns:
            A list of EntityBase objects representing all stored entities.
        """
        raw_list = await self.accessor.get_all()
        entities: List[EntityBase] = []

        for raw_dict in raw_list:
            raw_dict["ID"] = raw_dict.pop("_id", None)
            entity = parse_obj_as(EntityResponse, raw_dict)
            entities.append(entity)

        return entities

    async def get_entity_by_id(self, entity_id: str):
        """
        Retrieve a single entity by its unique identifier.

        Args:
            entity_id: The unique ID of the entity.

        Returns:
            The EntityBase instance if found, otherwise None.
        """
        raw_dict = await self.accessor.get_by_id(entity_id)
        if raw_dict is None:
            return None

        # MongoDB _id -> Pydantic ID
        raw_dict["ID"] = raw_dict.pop("_id", None)

        # Parse into correct Pydantic subclass
        entity = parse_obj_as(EntityResponse, raw_dict)
        return entity

    async def create_entity(self, entity: EntityBase):
        """
        Create a new entity in the system.

        Args:
            entity: The entity instance to be created.

        Returns:
            True if the entity was created, False otherwise.
        """
        entity_dict = entity.model_dump()

        try:
            await self.accessor.create(entity)
        except DuplicateKeyError as e:
            raise Exception(settings.INSERT_EVENT_FAILED % e)

        await self.send_to_socket(entity)
        entity_dict["ID"] = entity.ID
        return parse_obj_as(EntityResponse, entity_dict)

    async def send_to_socket(self, entity):
        """
        Emit an 'entity_created' event via Unix socket
        to notify the processing service.

        Args:
            entity: The entity instance to be created.

        Returns:
            True if the entity was sent to socket, False otherwise.
        """
        try:
            await self.socket_client.send({"id": entity.ID, "type": entity.type})
            return True
        except Exception as e:
            raise Exception(settings.SEND_EVENT_FAILED % e)

    async def delete_entity(self, entity_id: str) -> bool:
        """
        Delete an entity from the system.

        Args:
            entity_id: The unique ID of the entity to delete.

        Returns:
            True if the entity was deleted, False otherwise.
        """
        return await self.accessor.delete(entity_id)
