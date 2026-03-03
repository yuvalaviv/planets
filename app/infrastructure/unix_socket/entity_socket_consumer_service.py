# app/processing/entity_socket_consumer_service.py
import asyncio
from typing import Dict, Type

from app.accessors.entity_mongo_accessor import EntityMongoAccessor
from app.models.tree import Tree
from app.models.animal import Animal


class EntitySocketConsumerService:
    def __init__(self, entity_accessor: EntityMongoAccessor):
        self.entity_accessor = entity_accessor

        # Registry of entity types → domain classes
        self.entity_registry: Dict[str, Type] = {
            "Tree": Tree,
            "Animal": Animal,
        }

        # Keep track of running tasks to avoid duplicates
        self.running_tasks: Dict[str, asyncio.Task] = {}

    async def handle_message(self, message: dict) -> dict:
        """
        Handles incoming messages from UnixSocketServer
        """
        event = message.get("event")
        if event != "entity_created":
            return {"status": "ignored"}

        entity_id = message.get("entity_id")
        entity_data = await self.entity_accessor.get_by_id(entity_id)
        print(entity_data)
        if not entity_data:
            return {"status": "entity_not_found"}

        animal = Animal(**entity_data)
        print(self.entity_accessor)
        asyncio.create_task(animal.process(self.entity_accessor))  # start all tasks concurrently

    async def start_entity_process(self, entity):
        """
        Run the entity's async process method
        """
        if hasattr(entity, "process"):
            await entity.process()
        else:
            print(f"No process method defined for {entity.type}")