# app/routes/entity_route.py
from fastapi import APIRouter
from typing import List
from app.models.entity import Entity
from app.services.entity_service import EntityService


class EntityRoute:
    def __init__(self, service: EntityService):
        self.service = service
        self.router = APIRouter()
        self._setup_routes()

    def _setup_routes(self):
        self.router.add_api_route("/", self.get_all_entities, methods=["GET"], response_model=List[Entity])
        self.router.add_api_route("/{entity_id}", self.get_entity_by_id, methods=["GET"], response_model=Entity)
        self.router.add_api_route("/", self.create_entity, methods=["POST"])
        self.router.add_api_route("/{entity_id}", self.delete_entity, methods=["DELETE"])

    async def get_all_entities(self):
        return await self.service.get_all_entities()

    async def get_entity_by_id(self, entity_id: str):
        entity = await self.service.get_entity_by_id(entity_id)
        if entity:
            return entity
        return {"error": "Entity not found"}

    async def create_entity(self, entity: Entity):
        await self.service.create_entity(entity)
        return {"status": "created"}

    async def delete_entity(self, entity_id: str):
        await self.service.delete_entity(entity_id)
        return {"status": "deleted"}
