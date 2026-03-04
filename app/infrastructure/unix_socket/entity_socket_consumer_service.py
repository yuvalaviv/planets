import asyncio
from typing import Dict, Type, Any

from app.accessors.entity_mongo_accessor import EntityMongoAccessor
from app.config import settings
from app.models.tree import Tree
from app.models.animal import Animal
from app.services.lifecycle.animal_config import AnimalConfig
from app.services.lifecycle.animal_life_cycle_service import AnimalLifecycleService


class EntitySocketConsumerService:
    """
    Service responsible for handling messages received from the Unix socket server.

    This service acts as a consumer for asynchronous events (e.g., entity lifecycle events).
    Based on the entity type, it dynamically instantiates the correct domain model
    and triggers its processing logic.

    Responsibilities:
        - Fetch entity data from persistence layer.
        - Resolve the correct domain model using a registry.
        - Execute entity-specific async processing logic.
    """

    def __init__(self, entity_accessor: EntityMongoAccessor):
        """
        Initialize the consumer service.

        Args:
            entity_accessor (EntityMongoAccessor):
                Data access layer used to retrieve and update entity data.
        """
        self.entity_accessor = entity_accessor

        self.entity_registry: Dict[str, Type[Any]] = {
            "Tree": Tree,
            "Animal": Animal,
        }

    async def handle_message(self, message: dict) -> None:
        """
        Handle an incoming socket message.

        Expected message format:
            {
                "id": "<entity_id>",
                "type": "<entity_type>"
            }

        Workflow:
            1. Retrieve entity data from database.
            2. Determine correct entity class from registry.
            3. Instantiate domain object.
            4. Trigger async processing logic in background.

        Args:
            message (dict):
                Incoming message containing entity identification data.

        Raises:
            ValueError:
                If entity type is unsupported or entity not found.
        """
        entity_id = message.get("id")
        entity_type = message.get("type")

        if not entity_id or not entity_type:
            raise ValueError("Message must contain 'id' and 'type' fields.")

        entity_data = await self.entity_accessor.get_by_id(entity_id)

        if not entity_data:
            raise ValueError(f"Entity with ID {entity_id} not found.")

        entity_class = self.entity_registry.get(entity_type)

        if not entity_class:
            raise ValueError(f"Unsupported entity type: {entity_type}")

        entity_instance = entity_class(**entity_data)

        animal_config = AnimalConfig(
            age_increment=settings.GETTING_OLD,
            hunger_increment=settings.GETTING_HUNGRY,
            max_hunger=settings.MAX_HUNGRY,
            interval=settings.ENTITY_INTERVAL_SECONDS
        )

        lifecycle_service = AnimalLifecycleService(self.entity_accessor, animal_config)

        # Start lifecycle for one animal
        asyncio.create_task(lifecycle_service.run(entity_instance))