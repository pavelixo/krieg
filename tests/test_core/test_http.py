import pytest
from krieg.core.http import HTTP

@pytest.mark.asyncio
async def test_handle(mocker):
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

    http = HTTP()
    await http.handle(scope, receive, send)

    send.assert_has_awaits([
        mocker.call({
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"Content-Type", b"application/json")],
        }),
        mocker.call({"type": "http.response.body", "body": b"Hello World!"})
    ])
