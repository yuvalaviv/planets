from fastapi import APIRouter, HTTPException, status
from typing import List

from app.schema.entity_schema import EntityResponse
from app.services.entity_service import EntityService
from app.config import settings


class EntityRoute:
    """
    FastAPI route wrapper for entity-related endpoints.

    This class registers CRUD API endpoints for Entity management and delegates
    all business logic to the provided EntityService.
    """

    def __init__(self, service: EntityService):
        """
        Initialize EntityRoute with the service dependency.

        Args:
            service: EntityService instance for handling business logic.
        """
        self.service = service
        self.router = APIRouter()
        self._setup_routes()

    def _setup_routes(self):
        """Register all CRUD routes with the FastAPI router."""
        self.router.add_api_route(
            "/", self.get_all_entities, methods=["GET"], status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "/{entity_id}", self.get_entity_by_id, methods=["GET"], status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "/", self.create_entity, methods=["POST"], status_code=status.HTTP_201_CREATED
        )
        self.router.add_api_route(
            "/{entity_id}", self.delete_entity, methods=["DELETE"], status_code=status.HTTP_204_NO_CONTENT
        )

    async def get_all_entities(self) -> List[EntityResponse]:
        """
        Retrieve all entities.

        Returns:
            A list of EntityResponse objects representing all entities.
        """
        return await self.service.get_all_entities()

    async def get_entity_by_id(self, entity_id: str) -> EntityResponse:
        """
        Retrieve a single entity by its unique ID.

        Args:
            entity_id: The unique identifier of the entity.

        Returns:
            The EntityResponse object if found.

        Raises:
            HTTPException 404 if the entity does not exist.
        """
        entity = await self.service.get_entity_by_id(entity_id)

        if entity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=settings.NOT_FOUND_ERROR % entity_id
            )
        return entity

    async def create_entity(self, entity: EntityResponse) -> EntityResponse:
        """
        Create a new entity.

        Args:
            entity: The request payload containing entity data (without ID).

        Returns:
            The created EntityResponse object with assigned ID.

        Raises:
            HTTPException 400 if creation fails.
        """
        try:
            return await self.service.create_entity(entity)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=settings.CREATION_FAILED % e
            )

    async def delete_entity(self, entity_id: str):
        """
        Delete an entity by its ID.

        Args:
            entity_id: The unique identifier of the entity to delete.

        Returns:
            HTTP 204 No Content on successful deletion.

        Raises:
            HTTPException 404 if the entity does not exist.
        """
        deleted = await self.service.delete_entity(entity_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=settings.NOT_FOUND_ERROR % entity_id
            )
