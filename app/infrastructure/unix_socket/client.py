import asyncio
import json


class UnixSocketClient:
    """
    Asynchronous Unix socket client for sending JSON messages to a server.

    This client connects to a specified socket path (or host/port for testing),
    sends a JSON-encoded message, waits for a JSON response, and then closes
    the connection.

    Attributes:
        host (str): Host address.
        port (int): port number.
    """

    def __init__(self, host: str, port: int):
        """
        Initialize the UnixSocketClient.

        Args:
            host (str): Host address.
            port (int): port number.
        """
        self.host = host
        self.port = port

    async def send(self, message: dict) -> dict:
        """
        Send a JSON message to the socket server and receive the response.

        Args:
            message (dict): A dictionary representing the message to send.

        Returns:
            dict: The response received from the server, parsed from JSON.

        Raises:
            ConnectionError: If the connection to the server fails.
            json.JSONDecodeError: If the server response is not valid JSON.
        """
        # Note: currently connecting to localhost TCP (127.0.0.1:12345) for testing
        reader, writer = await asyncio.open_connection(self.host, self.port)

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
