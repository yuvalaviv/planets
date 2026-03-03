from fastapi import APIRouter
from services.planet_service import PlanetService
from models.planet import PlanetModel

router = APIRouter()
planet_service = PlanetService(...)  # inject accessor

@router.get("/planets")
async def get_all_planets():
    return await planet_service.get_all_planets()

@router.post("/planets")
async def create_planet(planet: PlanetModel):
    await planet_service.create_planet(planet)
    return {"status": "created"}

@router.get("/planets/{planet_id}")
async def get_planet_by_id(planet_id: str):
    return await planet_service.get_planet_by_id(planet_id)

@router.delete("/planets/{planet_id}")
async def delete_planet(planet_id: str):    
    await planet_service.delete_planet(planet_id)
    return {"status": "deleted"}