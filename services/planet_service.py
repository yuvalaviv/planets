from models.planet import Planet

class PlanetService:
    def __init__(self, accessor):
        self.accessor = accessor

    async def get_all_planets(self):
        return await self.accessor.get_all()

    async def create_planet(self, planet_model: Planet):
        await self.accessor.create(planet_model)

    async def get_planet_by_id(self, planet_id: str):
        return await self.accessor.get_by_id(planet_id)
    
    async def delete_planet(self, planet_id: str):
        await self.accessor.delete(planet_id)
        