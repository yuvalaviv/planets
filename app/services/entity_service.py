# app/services/entity_service.py
from app.accessors.entity_mongo_accessor import EntityMongoAccessor
from app.models.entity import Entity
from typing import List, Optional


class EntityService:
    def __init__(self, accessor: EntityMongoAccessor):
        self.accessor = accessor

    async def get_all_entities(self) -> List[Entity]:
        return await self.accessor.get_all()

    async def get_entity_by_id(self, entity_id: str) -> Optional[Entity]:
        return await self.accessor.get_by_id(entity_id)

    async def create_entity(self, entity: Entity):
        await self.accessor.create(entity)

    async def delete_entity(self, entity_id: str):
        await self.accessor.delete(entity_id)