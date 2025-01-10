from typing import Dict, Any
from krieg.core.headers import Header
from krieg.core.types import ASGISendCallable


class Response:
    def __init__(self, status: int = 200, headers: Dict[str, str] = None, body: bytes = b""):
        """
        Initializes the Response object.

        :param status: The HTTP status code of the response (default: 200).
        :param headers: A dictionary of response headers (default: None).
        :param body: The body of the response as bytes (default: empty bytes).
        """
        self.status = status
        headers = [(key.encode("utf-8"), value.encode("utf-8")) for key, value in (headers or {}).items()]
        self.headers = Header(headers)
        self.body = body

    def to_asgi(self) -> Dict[str, Any]:
        """
        Converts the response into an ASGI-compatible format.

        :return: A dictionary containing ASGI-compatible response headers and status.
        """
        return {
            "type": "http.response.start",
            "status": self.status,
            "headers": self.headers.get_headers(),
        }

    async def send(self, send: ASGISendCallable):
        """
        Sends the response.

        :param send: ASGI send callable to send the response.
        """
        # Send the header portion of the response
        await send(self.to_asgi())
        # Send the body portion of the response
        await send({"type": "http.response.body", "body": self.body})
