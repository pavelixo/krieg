from typing import Callable, Awaitable
from krieg.core.responses import Response
from krieg.core.requests import Request
from krieg.utils.datastructures import MultiValueDict, OrderedSet


class Router:
    def __init__(self):
        # Use MultiValueDict to allow multiple handlers per route
        self.http_routes = MultiValueDict()
        self.ws_routes = MultiValueDict()

    def add_http_route(self, method: str, path: str, handler: Callable[[Request], Awaitable[Response]]):
        """Adds a route with a handler."""
        self.http_routes.add((method, path), handler)

    def get_http_handler(self, method: str, path: str) -> Callable[[Request], Awaitable[Response]]:
        """Retrieves the first handler for the specified method and path."""
        handlers = self.http_routes.get((method, path))
        if handlers:
            return handlers[0]  # Return the first handler
        return None
    
    def add_ws_route(self, path: str, handler: Callable):
        self.ws_routes.add(path, handler)

    def get_ws_handler(self, path: str) -> Callable:
        handlers = self.ws_routes.get(path)
        if handlers:
            return handlers[0]
        return None

    def __iter__(self):
        """Iterates over the keys of the dictionary, which represent the http_routes."""
        return self.http_routes.__iter__()

    def __repr__(self):
        """String representation of the Router."""
        return f"Router(http_routes={self.http_routes}, route_order={self.route_order})"
