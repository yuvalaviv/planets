"""
run_consumer.py

Application entry point for the Unix socket consumer service.

This module initializes:
    - MongoDB async client (Motor)
    - Entity data accessor
    - Entity socket consumer service
    - Unix socket server

The server listens for incoming socket messages and delegates
processing to EntitySocketConsumerService.

This script is intended to be executed as a standalone process:

    python run_consumer.py
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from app.accessors.entity_mongo_accessor import EntityMongoAccessor
from app.infrastructure.unix_socket.entity_socket_consumer_service import EntitySocketConsumerService
from app.infrastructure.unix_socket.server import UnixSocketServer
from app.config import settings
from app.services.lifecycle.animal_config import AnimalConfig
from app.services.lifecycle.animal_life_cycle_service import AnimalLifecycleService


async def main():
    """
    Initialize and start the Unix socket consumer server.

    Workflow:
        1. Establish asynchronous MongoDB connection.
        2. Create data access layer (EntityMongoAccessor).
        3. Initialize the socket consumer service.
        4. Start the UnixSocketServer with injected message handler.

    This function runs indefinitely until the process is terminated.

    Raises:
        Exception:
            Propagates any startup failure such as database connection
            errors or socket binding issues.
    """
    client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    db = client[settings.MONGO_DB]

    accessor = EntityMongoAccessor(db)

    consumer_service = EntitySocketConsumerService(accessor)

    server = UnixSocketServer(
        socket_path=settings.SOCKET_PATH,
        hostname=settings.SOCKET_HOSTNAME,
        port=settings.SOCKET_PORT,
        message_handler=consumer_service.handle_message
    )

    await server.start()

if __name__ == "__main__":
    """
    Entry point for running the consumer as a standalone process.

    Uses asyncio.run() to start the async event loop and execute main().
    """
    asyncio.run(main())
