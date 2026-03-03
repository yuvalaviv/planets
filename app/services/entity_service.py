# app/services/entity_service.py
from app.accessors.entity_mongo_accessor import EntityMongoAccessor
from app.infrastructure.unix_socket.client import UnixSocketClient
from app.models.base_entity import EntityBase
from typing import List, Optional


class EntityService:
    def __init__(self, accessor: EntityMongoAccessor, socket_path: str):
        self.accessor = accessor
        self.socket_client = UnixSocketClient(socket_path)

    async def get_all_entities(self) -> List[EntityBase]:
        return await self.accessor.get_all()

    async def get_entity_by_id(self, entity_id: str) -> Optional[EntityBase]:
        return await self.accessor.get_by_id(entity_id)

    async def create_entity(self, entity: EntityBase):
        # 1. Save to DB
        try:
            await self.accessor.create(entity)
        except Exception as e:
            print("Failed to create entity in DB:", e)

        # 2. Send event to socket server
        try:
            await self.socket_client.send({
                "event": "entity_created",
                "entity_id": entity.ID,
                "type": entity.type
            })
        except Exception as e:
            print("Failed to send entity_created event:", e)

    async def delete_entity(self, entity_id: str):
        await self.accessor.delete(entity_id)
