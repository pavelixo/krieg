from asyncio import to_thread
from inspect import iscoroutinefunction
from functools import wraps
from typing import Callable, Awaitable
from krieg.core.router import Router
from krieg.core.websocket import WebSocket
from krieg.core.responses import Response
from krieg.core.requests import Request
from krieg.core.types import Scope, ASGIReceiveCallable, ASGISendCallable


class Application:
    def __init__(self):
        self._router = Router()

    async def __call__(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable):
        await self._handler(scope)(scope, receive, send)

    def websocket(self, path: str):
        """Decorator for WebSocket routes."""
        return self._create_websocket(path)
 
    def get(self, path: str):
        """Decorator for GET routes."""
        return self._create_http("GET", path)

    def post(self, path: str):
        """Decorator for POST routes."""
        return self._create_http("POST", path)

    def put(self, path: str):
        """Decorator for PUT routes."""
        return self._create_http("PUT", path)

    def delete(self, path: str):
        """Decorator for DELETE routes."""
        return self._create_http("DELETE", path)

    def patch(self, path: str):
        """Decorator for PATCH routes."""
        return self._create_http("PATCH", path)

    def options(self, path: str):
        """Decorator for OPTIONS routes."""
        return self._create_http("OPTIONS", path)

    def head(self, path: str):
        """Decorator for HEAD routes."""
        return self._create_http("HEAD", path)

    def _handler(self, scope: Scope):
        handlers = {"http": self._get_http_handler, "websocket": self._get_ws_handler}
        return handlers[scope["type"]]
    
    async def _get_http_handler(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable):
        # Retrieves the appropriate route handler
        method = scope["method"]
        path = scope["path"]
        handler = self._router.get_http_handler(method, path)

        if handler:
            request = Request(scope, receive)
            if not iscoroutinefunction(handler):
                response = await to_thread(handler, request)
            else:
                response = await handler(request) 
            
            await response.send(send)

    async def _get_ws_handler(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable):
        """Handles WebSocket connections."""
        path = scope["path"]
        handler = self._router.get_ws_handler(path)

        if handler:
            websocket = WebSocket(scope, receive, send)
            await websocket.accept()
            await handler(websocket)

    def _create_http(self, method: str, path: str):
        """Creates a decorator for associating routes and HTTP methods."""
        def decorator(func: Callable[[Request], Awaitable[Response]]):
            @wraps(func)
            async def wrapper(request: Request) -> Response:
                # Wrapper function that simply calls the original handler
                if not iscoroutinefunction(func):
                    return await to_thread(func, request)
                
                return await func(request)
            
            # Registers the route with the _router
            self._router.add_http_route(method, path, func)
            return wrapper
        return decorator

    def _create_websocket(self, path: str):
        """Creates a decorator for WebSocket"""
        def decorator(func: Callable[[WebSocket], Awaitable[None]]):
            self._router.add_ws_route(path, func)
            return func
        return decorator
