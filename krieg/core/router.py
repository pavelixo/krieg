from typing import Callable, Awaitable
from krieg.core.responses import Response
from krieg.core.requests import Request


class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, method: str, path: str, handler: Callable[[Request], Awaitable[Response]]):
        self.routes.append((method, path, handler))

    def get_handler(self, method: str, path: str) -> Callable[[Request], Awaitable[Response]]:
        for route_method, route_path, handler in self.routes:
            if route_method == method and route_path == path:
                return handler
        return None
