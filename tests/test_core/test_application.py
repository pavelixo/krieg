import pytest
from krieg.core.application import Application
from krieg.core.responses import Response
from krieg.core.requests import Request
from krieg.core.types import Scope, ASGIReceiveCallable, ASGISendCallable

@pytest.mark.asyncio
async def test_application_call(mocker):
    app = Application()
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/test",
        "headers": [(b"Content-Type", b"application/json")],
    }
    receive = mocker.AsyncMock(side_effect=[
        {"type": "http.request", "body": b"Hello", "more_body": True},
        {"type": "http.request", "body": b" World!", "more_body": False},
    ])
    send = mocker.AsyncMock()

    async def handler(request: Request) -> Response:
        return Response(body=b"Hello, World!", headers={"Content-Type": "application/json"})

    app.add_route("GET", "/test", handler)
    await app(scope, receive, send)

    send.assert_has_awaits([
        mocker.call({
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"Content-Type", b"application/json")],
        }),
        mocker.call({"type": "http.response.body", "body": b"Hello, World!"})
    ])
