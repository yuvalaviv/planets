# app/main.py

import uvicorn

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.accessors.entity_mongo_accessor import EntityMongoAccessor
from app.infrastructure.unix_socket.client import UnixSocketClient
from app.routes.entity_route import EntityRoute
from app.routes.planet_route import PlanetRoute
from app.accessors.planet_mongo_accessor import PlanetMongoAccessor
from app.services.entity_service import EntityService
from app.services.planet_service import PlanetService

# FastAPI instance
app = FastAPI(title="Planet API", version="1.0")

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["universe"]
socket_client = UnixSocketClient("/tmp/entity.sock")

# Initialize Accessor and Service
mongo_accessor = PlanetMongoAccessor(db)
planet_service = PlanetService(mongo_accessor)
planet_route = PlanetRoute(planet_service)

entity_accessor = EntityMongoAccessor(db)
entity_service = EntityService(entity_accessor, socket_client)
entity_route = EntityRoute(entity_service)



# Include Routes
app.include_router(planet_route.router, prefix="/planets", tags=["planets"])
app.include_router(entity_route.router, prefix="/entities", tags=["entities"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
