import pytest
from typing import Callable, Awaitable
from krieg.core.router import Router
from krieg.core.responses import Response
from krieg.core.requests import Request

@pytest.mark.asyncio
async def test_add_route():
    router = Router()
    async def handler(request: Request) -> Response:
        return Response(body=b"Hello, World!")

    router.add_route("GET", "/test", handler)
    assert len(router.routes) == 1
    assert router.routes[0] == ("GET", "/test", handler)

@pytest.mark.asyncio
async def test_get_handler():
    router = Router()
    async def handler(request: Request) -> Response:
        return Response(body=b"Hello, World!")

    router.add_route("GET", "/test", handler)
    handler_found = router.get_handler("GET", "/test")
    assert handler_found == handler

    handler_not_found = router.get_handler("POST", "/test")
    assert handler_not_found is None
