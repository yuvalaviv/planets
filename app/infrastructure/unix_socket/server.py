import asyncio
import json
import os
from typing import Callable, Awaitable
from app.config import settings


class UnixSocketServer:
    """
    Asynchronous Unix domain socket server for handling JSON-based messages.

    The server listens on a Unix socket file and delegates incoming messages
    to an injected async message handler.

    Responsibilities:
        - Accept client connections.
        - Read newline-delimited JSON messages.
        - Delegate message processing to a provided async handler.
        - Send JSON responses back to the client.
        - Gracefully handle client disconnects and errors.
    """
    def __init__(self, socket_path: str, hostname: str, port: int, message_handler: Callable[[dict], Awaitable[dict]]):
        """
        Initialize the UnixSocketServer.

        Args:
            socket_path (str): Filesystem path to the Unix socket.
            hostname: Host address
            port: Port number
            message_handler (Callable[[dict], Awaitable[dict]]):
                Async function responsible for processing incoming messages.
                Must accept a dictionary and return a dictionary response.
        """
        self.socket_path = socket_path
        self.message_handler = message_handler
        self.hostname = hostname
        self.port = port
        self.server = None

    async def start(self):
        """
        Start the Unix socket server.

        This method:
            1. Removes any existing socket file.
            2. Creates a new Unix socket server.
            3. Begins serving clients indefinitely.

        Raises:
            OSError: If socket cannot be created.
        """
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)

        self.server = await asyncio.start_server(self._handle_client, host=self.hostname, port=self.port)

        print(settings.RUNNING_UNIX % {self.socket_path})

        async with self.server:
            await self.server.serve_forever()

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        Handle a single client connection.

        This method:
            - Continuously reads newline-delimited JSON messages.
            - Calls the injected message handler.
            - Sends back JSON responses.
            - Handles client disconnects gracefully.

        Args:
            reader (asyncio.StreamReader): Client input stream.
            writer (asyncio.StreamWriter): Client output stream.
        """
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break

                message = json.loads(data.decode())
                response = await self.message_handler(message)

                writer.write(json.dumps(response).encode() + b"\n")
                await writer.drain()

        except Exception as e:
            print(settings.SERVER_ERROR % e)
        finally:
            writer.close()
            await writer.wait_closed()
