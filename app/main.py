"""
Main entry point and composition root for Planet & Entity API.

Responsibilities:
    - Initialize database connections asynchronously.
    - Wire application services with accessors and infrastructure.
    - Setup API routes and mount them with prefixes and tags.
    - Manage graceful startup and shutdown events.
    - Run FastAPI application via Uvicorn (dev/prod aware).
"""

import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.accessors.entity_mongo_accessor import EntityMongoAccessor
from app.accessors.planet_mongo_accessor import PlanetMongoAccessor
from app.infrastructure.unix_socket.client import UnixSocketClient
from app.services.entity_service import EntityService
from app.services.planet_service import PlanetService
from app.routes.entity_route import EntityRoute
from app.routes.planet_route import PlanetRoute


app = FastAPI(title="Planet API", version="1.0")


@app.on_event("startup")
async def startup():
    """
    Startup event: Initialize DB client, accessors, services, and routes.
    """
    # MongoDB client
    app.state.db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    db = app.state.db_client[settings.MONGO_DB]

    # Infrastructure clients
    app.state.socket_client = UnixSocketClient(settings.SOCKET_HOSTNAME, settings.SOCKET_PORT)

    # Accessors
    app.state.planet_accessor = PlanetMongoAccessor(db)
    app.state.entity_accessor = EntityMongoAccessor(db)

    # Services
    app.state.planet_service = PlanetService(app.state.planet_accessor)
    app.state.entity_service = EntityService(app.state.entity_accessor, app.state.socket_client)

    # Routes
    planet_router = PlanetRoute(app.state.planet_service).router
    entity_router = EntityRoute(app.state.entity_service).router

    app.include_router(planet_router, prefix="/planets", tags=["planets"])
    app.include_router(entity_router, prefix="/entities", tags=["entities"])


@app.on_event("shutdown")
async def shutdown():
    """
    Shutdown event: Close DB client and cleanup resources.
    """
    if hasattr(app.state, "db_client"):
        app.state.db_client.close()


if __name__ == "__main__":
    host = getattr(settings, "HOST", "127.0.0.1")
    port = getattr(settings, "PORT", 8000)
    reload_flag = getattr(settings, "ENV", "development") == "development"

    uvicorn.run("app.main:app", host=host, port=port, reload=reload_flag)