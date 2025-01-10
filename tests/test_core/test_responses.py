import pytest
from typing import Dict, Any
from krieg.core.headers import Header
from krieg.core.types import ASGISendCallable
from krieg.core.responses import Response

@pytest.mark.asyncio
async def test_response_initialization():
    response = Response(status=200, headers={"Content-Type": "application/json"}, body=b"Hello, World!")
    assert response.status == 200
    assert response.headers.get_header("Content-Type") == b"application/json"
    assert response.body == b"Hello, World!"

@pytest.mark.asyncio
async def test_to_asgi():
    response = Response(status=200, headers={"Content-Type": "application/json"}, body=b"Hello, World!")
    asgi_response = response.to_asgi()
    assert asgi_response == {
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"Content-Type", b"application/json")],
    }

@pytest.mark.asyncio
async def test_send(mocker):
    send_mock = mocker.AsyncMock()
    response = Response(status=200, headers={"Content-Type": "application/json"}, body=b"Hello, World!")

    await response.send(send_mock)

    send_mock.assert_has_awaits([
        mocker.call({
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"Content-Type", b"application/json")],
        }),
        mocker.call({"type": "http.response.body", "body": b"Hello, World!"})
    ])
