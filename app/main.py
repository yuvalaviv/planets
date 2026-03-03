# app/main.py

import uvicorn

from fastapi import FastAPI
from app.routes.planet_route import PlanetRoute
from app.accessors.planet_mongo_accessor import PlanetMongoAccessor
from app.services.planet_service import PlanetService

# FastAPI instance
app = FastAPI(title="Planet API", version="1.0")

# Initialize Accessor and Service
mongo_accessor = PlanetMongoAccessor(
    connection_string="mongodb://localhost:27017",
    database_name="universe"
)
planet_service = PlanetService(mongo_accessor)
planet_route = PlanetRoute(planet_service)

# Include Routes
app.include_router(planet_route.router, prefix="/planets", tags=["planets"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)