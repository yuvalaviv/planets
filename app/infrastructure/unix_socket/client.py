import asyncio
import json


class UnixSocketClient:
    def __init__(self, socket_path: str):
        self.socket_path = socket_path

    async def send(self, message: dict) -> dict:
        reader, writer = await asyncio.open_connection("127.0.0.1", 12345)

        try:
            # Send JSON message
            data = json.dumps(message).encode()
            writer.write(data + b"\n")
            await writer.drain()

            # Wait for response
            response_data = await reader.readline()
            response = json.loads(response_data.decode())

            return response

        finally:
            writer.close()
            await writer.wait_closed()
