from fastapi import APIRouter, HTTPException, status
from app.models.planet import PlanetModel
from app.services.planet_service import PlanetService
from typing import List


class PlanetRoute:
    """
    FastAPI route wrapper for planet-related endpoints.

    This class registers CRUD API endpoints for Planet management
    and delegates all business logic to the PlanetService.

    Endpoints:
        - GET "/" : Retrieve all planets.
        - GET "/{planet_id}" : Retrieve a single planet by ID.
        - POST "/" : Create a new planet.
        - DELETE "/{planet_id}" : Delete a planet by ID.
    """

    def __init__(self, planet_service: PlanetService):
        """
        Initialize PlanetRoute with the service dependency.

        Args:
            planet_service: PlanetService instance for handling business logic.
        """
        self.planet_service = planet_service
        self.router = APIRouter()
        self._setup_routes()

    def _setup_routes(self):
        """Register all CRUD routes with the FastAPI router."""
        self.router.add_api_route(
            "/", self.get_all_planets, methods=["GET"], response_model=List[PlanetModel]
        )
        self.router.add_api_route(
            "/{planet_id}", self.get_planet_by_id, methods=["GET"], response_model=PlanetModel
        )
        self.router.add_api_route(
            "/", self.create_planet, methods=["POST"], response_model=PlanetModel, status_code=status.HTTP_201_CREATED
        )
        self.router.add_api_route(
            "/{planet_id}", self.delete_planet, methods=["DELETE"], status_code=status.HTTP_204_NO_CONTENT
        )

    async def get_all_planets(self) -> List[PlanetModel]:
        """
        Retrieve all planets from the database.

        Returns:
            List[PlanetModel]: A list of all planets.
        """
        try:
            return await self.planet_service.get_all_planets()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve planets: {str(e)}"
            )

    async def get_planet_by_id(self, planet_id: str) -> PlanetModel:
        """
        Retrieve a single planet by its ID.

        Args:
            planet_id: The unique identifier of the planet.

        Returns:
            PlanetModel: The planet object if found.

        Raises:
            HTTPException 404 if the planet does not exist.
            HTTPException 500 for other errors.
        """
        planet = await self.planet_service.get_planet_by_id(planet_id)
        if planet is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Planet with ID {planet_id} not found"
            )
        return planet

    async def create_planet(self, planet: PlanetModel) -> PlanetModel:
        """
        Create a new planet.

        Args:
            planet: The PlanetModel object to be created.

        Returns:
            PlanetModel: The created planet object with assigned ID.

        Raises:
            HTTPException 400 if creation fails.
        """
        try:
            await self.planet_service.create_planet(planet)
            return planet
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create planet: {str(e)}"
            )

    async def delete_planet(self, planet_id: str):
        """
        Delete a planet by its ID.

        Args:
            planet_id: The unique identifier of the planet to delete.

        Returns:
            HTTP 204 No Content on success.

        Raises:
            HTTPException 404 if the planet does not exist.
            HTTPException 500 for other errors.
        """
        deleted = await self.planet_service.delete_planet(planet_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Planet with ID {planet_id} not found"
            )
