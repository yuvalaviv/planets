# app/routes/planet_route.py
from fastapi import APIRouter
from app.models.planet import PlanetModel
from app.services.planet_service import PlanetService
from typing import List

class PlanetRoute:
    def __init__(self, planet_service: PlanetService):
        self.planet_service = planet_service
        self.router = APIRouter()
        self._setup_routes()

    def _setup_routes(self):
        self.router.add_api_route("/", self.get_all_planets, methods=["GET"], response_model=List[PlanetModel])
        self.router.add_api_route("/{planet_id}", self.get_planet_by_id, methods=["GET"], response_model=PlanetModel)
        self.router.add_api_route("/", self.create_planet, methods=["POST"])
        self.router.add_api_route("/{planet_id}", self.delete_planet, methods=["DELETE"])

    # ========================
    # Route Handlers
    # ========================
    async def get_all_planets(self):
        return await self.planet_service.get_all_planets()

    async def get_planet_by_id(self, planet_id: str):
        return await self.planet_service.get_planet_by_id(planet_id)

    async def create_planet(self, planet: PlanetModel):
        await self.planet_service.create_planet(planet)
        return {"status": "created"}

    async def delete_planet(self, planet_id: str):
        await self.planet_service.delete_planet(planet_id)
        return {"status": "deleted"}