from typing import Callable, Awaitable
from krieg.core.router import Router
from krieg.core.http import HTTP
from krieg.core.websocket import WebSocket
from krieg.core.responses import Response
from krieg.core.requests import Request
from krieg.core.types import Scope, ASGIReceiveCallable, ASGISendCallable


class Application:
    def __init__(self):
        self.router = Router()

    async def __call__(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable):
        handler = self._get_handler(scope)
        self.http = HTTP()
        self.websocket = WebSocket()
        if handler:
            request = Request(scope, receive)
            response = await handler(request)
            await response.send(send)

    def _get_handler(self, scope: Scope) -> Callable[[Request], Awaitable[Response]]:
        method = scope.get("method", "").upper()
        path = scope.get("path", "")
        return self.router.get_handler(method, path)

    def add_route(self, method: str, path: str, handler: Callable[[Request], Awaitable[Response]]):
        self.router.add_route(method, path, handler)
