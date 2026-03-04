from typing import List, Optional

from app.accessors.planet_mongo_accessor import PlanetMongoAccessor
from app.models.planet import PlanetModel


class PlanetService:
    """
    Service layer responsible for managing Planet operations.

    This service abstracts the interaction with the persistence layer (accessor),
    providing high-level methods to retrieve, create, and delete planets.
    """

    def __init__(self, accessor: PlanetMongoAccessor):
        """
        Initialize the PlanetService with a data accessor.

        Args:
            accessor: The data access object responsible for persistence operations
                      for planets (e.g., PlanetMongoAccessor).
        """
        self.accessor = accessor

    async def get_all_planets(self) -> List[PlanetModel]:
        """
        Retrieve all planets from the database.

        Returns:
            A list of PlanetModel instances representing all stored planets.
        """
        return await self.accessor.get_all()

    async def create_planet(self, planet_model: PlanetModel) -> str:
        """
        Create a new planet in the database.

        Args:
            planet_model: An instance of PlanetModel representing the planet
                          to be created.

        Side Effects:
            Persists the planet in the database.
        """
        return await self.accessor.create(planet_model)

    async def get_planet_by_id(self, planet_id: str) -> Optional[PlanetModel]:
        """
        Retrieve a single planet by its unique identifier.

        Args:
            planet_id: The unique ID of the planet to retrieve.

        Returns:
            A PlanetModel instance if found, otherwise None.
        """
        return await self.accessor.get_by_id(planet_id)

    async def delete_planet(self, planet_id: str) -> bool:
        """
        Delete a planet from the database.

        Args:
            planet_id: The unique ID of the planet to delete.

        Returns:
            True if the entity was deleted, False otherwise.
        """
        return await self.accessor.delete(planet_id)
