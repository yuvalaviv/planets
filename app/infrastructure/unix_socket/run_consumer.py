# run_consumer.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from app.accessors.entity_mongo_accessor import EntityMongoAccessor
from app.infrastructure.unix_socket.entity_socket_consumer_service import EntitySocketConsumerService
from app.infrastructure.unix_socket.server import UnixSocketServer

SOCKET_PATH = "/tmp/entity.sock"


async def main():
    # Mongo setup
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["universe"]

    accessor = EntityMongoAccessor(db)

    # Service
    consumer_service = EntitySocketConsumerService(accessor)

    # Server
    server = UnixSocketServer(
        socket_path=SOCKET_PATH,
        message_handler=consumer_service.handle_message
    )
    await server.start()

asyncio.run(main())
