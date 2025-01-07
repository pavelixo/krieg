import re
import json
from typing import Callable, Any, Optional
from concurrent.futures import Executor
from aiohttp.web_app import Application
from krieg.requests import Request
from krieg.responses import Response
from krieg.types import LooseHeaders


class Krieg(Application):
    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes the Krieg class.

        Args:
            *args: Additional positional arguments for the base Application class.
            logger (logging.Logger): The logger to be used by the application. Default is web_logger.
            router (Optional[UrlDispatcher]): The URL router. Default is None.
            middlewares (Iterable[Middleware]): A list of middlewares to be applied. Default is an empty list.
            handler_args (Optional[Mapping[str, Any]]): Additional arguments for the handlers. Default is None.
            client_max_size (int): The maximum client size in bytes. Default is 1024**2 (1 MB).
            loop (Optional[asyncio.AbstractEventLoop]): The asyncio event loop to be used. Default is None.
            debug (Any): Debug mode. Default is ... (mypy doesn't support ellipsis).
            **kwargs: Additional keyword arguments for the base Application class.
        """
        super().__init__(*args, **kwargs)
        self._routes = {}  # Initialize the routes dictionary

    def _response(
        self,
        *,
        body: Any = None,
        status: int = 200,
        reason: Optional[str] = None,
        text: Optional[str] = None,
        headers: Optional[LooseHeaders] = None,
        content_type: Optional[str] = "application/octet-stream",
        charset: Optional[str] = None,
        zlib_executor_size: Optional[int] = None,
        zlib_executor: Optional[Executor] = None,
    ) -> Response:
        if isinstance(body, dict):
            content_type = "application/json"
            body = json.dumps(body)

        if isinstance(body, str):
            html_pattern = re.compile(r'<(\"[^\"]*\"|\'[^\']*\'|[^\'\">])*>')
            if html_pattern.search(body):
                content_type = "text/html"
            else:
                content_type = "text/plain"

        response = Response(
            body=body,
            status=status,
            reason=reason,
            text=text,
            headers=headers,
            content_type=content_type,
            charset=charset
        )

        if zlib_executor is not None:
            response.enable_compression(zlib_executor, zlib_executor_size)

        return response

    def _create_route(self, method: str) -> Callable:
        def decorator(path: str) -> Callable:
            def wrapper(func: Callable) -> Callable:
                async def wrapped_func(request: Request) -> Response:
                    result = await func(request)
                    return self._response(body=result)

                self._routes[path] = (method, wrapped_func)  # Store the route in the dictionary
                self.router.add_route(method, path, wrapped_func)  # Add the route to the router
                return func

            return wrapper

        return decorator

    def get(self, path: str) -> Callable:
        return self._create_route("GET")(path)

    def post(self, path: str) -> Callable:
        return self._create_route("POST")(path)

    def put(self, path: str) -> Callable:
        return self._create_route("PUT")(path)

    def delete(self, path: str) -> Callable:
        return self._create_route("DELETE")(path)

    def patch(self, path: str) -> Callable:
        return self._create_route("PATCH")(path)

    def options(self, path: str) -> Callable:
        return self._create_route("OPTIONS")(path)

    def head(self, path: str) -> Callable:
        return self._create_route("HEAD")(path)

    def trace(self, path: str) -> Callable:
        return self._create_route("TRACE")(path)