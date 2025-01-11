from typing import Dict
from krieg.core.headers import Header
from krieg.core.types import Scope, ASGIReceiveCallable


class Request:
    def __init__(self, scope: Scope, receive: ASGIReceiveCallable):
        """
        Initializes the Request object.

        :param scope: The ASGI scope containing request metadata.
        :param receive: The ASGI receive callable for receiving request messages.
        """
        self.scope = scope
        self.receive = receive

        # Initialize the header manager with the headers from the ASGI scope
        headers = scope.get("headers", [])
        self.header = Header(headers)

    async def body(self) -> bytes:
        """
        Retrieves the full request body as bytes.

        :return: The request body.
        """
        body_data = b""

        async for message in self._receive_messages():
            body_data += message.get("body", b"")

        return body_data

    async def _receive_messages(self):
        """
        Generator to receive messages asynchronously.

        :yield: Each message received.
        """
        more_body = True

        while more_body:
            message = await self.receive()
            yield message
            more_body = message.get("more_body", False)

    @property
    def headers(self) -> Dict[bytes, bytes]:
        """
        Returns the headers as a dictionary.

        :return: A dictionary of headers where both keys and values are bytes.
        """
        # Instead of directly using a list of headers, we now rely on the MultiValueDict
        return {key: value for key, value in self.header.get_headers()}

    @property
    def method(self) -> str:
        """
        Returns the HTTP method of the request.

        :return: The HTTP method (e.g., "GET", "POST").
        """
        return self.scope.get("method", "").upper()

    @property
    def path(self) -> str:
        """
        Returns the URL path of the request.

        :return: The URL path.
        """
        return self.scope.get("path", "")

    def add_header(self, name: str, value: str):
        """
        Adds a new header to the request.

        :param name: The name of the header.
        :param value: The value of the header.
        """
        self.header.add_header(name, value)

    def remove_header(self, name: str):
        """
        Removes a header from the request.

        :param name: The name of the header to be removed.
        """
        self.header.remove_header(name)

    def set_header(self, name: str, value: str):
        """
        Sets or updates a header in the request.

        :param name: The name of the header.
        :param value: The value of the header.
        """
        self.header.set_header(name, value)
