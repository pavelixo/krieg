from typing import Dict, Any, List, Tuple, Union
from krieg.core.headers import Header
from krieg.core.types import ASGISendCallable

class Response:
    def __init__(self, status: int = 200, headers: Union[Dict[str, str], List[Tuple[bytes, bytes]]] = None, body: bytes = b""):
        """
        Initializes the Response object.

        :param status: The HTTP status code of the response (default: 200).
        :param headers: A dictionary or list of tuples of response headers (default: None).
        :param body: The body of the response as bytes (default: empty bytes).
        """
        self.status = status
        self.headers = Header(self._convert_headers(headers) if headers else [])
        self.body = body

    def _convert_headers(self, headers: Union[Dict[str, str], List[Tuple[bytes, bytes]]]) -> List[Tuple[bytes, bytes]]:
        """
        Converts headers to a list of tuples of bytes.

        :param headers: A dictionary or list of tuples of headers.
        :return: A list of tuples of bytes.
        """
        if isinstance(headers, dict):
            return [(key.encode() if isinstance(key, str) else key, value.encode() if isinstance(value, str) else value) for key, value in headers.items()]
        elif isinstance(headers, list):
            return headers
        else:
            raise ValueError("Headers must be a dictionary or a list of tuples.")

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
