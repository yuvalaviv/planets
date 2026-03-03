# app/infrastructure/unix_socket/server.py
import asyncio
import json
import os
from typing import Callable, Awaitable


class UnixSocketServer:
    def __init__(self, socket_path: str, message_handler: Callable[[dict], Awaitable[dict]]):
        """
        :param socket_path: Path to Unix socket file
        :param message_handler: async function that receives dict and returns dict response
        """
        self.socket_path = socket_path
        self.message_handler = message_handler
        self.server = None

    async def start(self):
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)
        self.server = await asyncio.start_server(
            self._handle_client,
            host="127.0.0.1",
            port=12345
        )

        print(f"UnixSocketServer running on {self.socket_path}")

        async with self.server:
            await self.server.serve_forever()

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break  # client disconnected

                message = json.loads(data.decode())
                print(message)
                # Call the injected handler
                response = await self.message_handler(message)

                writer.write(json.dumps(response).encode() + b"\n")
                await writer.drain()

        except Exception as e:
            print("Server error:", e)
        finally:
            writer.close()
            await writer.wait_closed()