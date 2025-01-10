from functools import wraps
from typing import Callable, Awaitable
from krieg.core.responses import Response
from krieg.core.requests import Request

def create_http_method_decorator(method: str, path: str):
    def decorator(func: Callable[[Request], Awaitable[Response]]):
        @wraps(func)
        async def wrapper(request: Request) -> Response:
            return await func(request)
        wrapper.method = method
        wrapper.path = path
        return wrapper
    return decorator

get = lambda path: create_http_method_decorator("GET", path)
post = lambda path: create_http_method_decorator("POST", path)
put = lambda path: create_http_method_decorator("PUT", path)
delete = lambda path: create_http_method_decorator("DELETE", path)
patch = lambda path: create_http_method_decorator("PATCH", path)
options = lambda path: create_http_method_decorator("OPTIONS", path)
head = lambda path: create_http_method_decorator("HEAD", path)