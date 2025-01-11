import pytest
from krieg.core.requests import Request

@pytest.mark.asyncio
async def test_request_initialization():
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/test",
        "headers": [(b"Content-Type", b"application/json")],
    }
    receive = lambda: {}
    request = Request(scope, receive)

    assert request.method == "GET"
    assert request.path == "/test"
    assert request.headers == {b"Content-Type": b"application/json"}

@pytest.mark.asyncio
async def test_request_body(mocker):
    scope = {
        "type": "http",
        "method": "POST",
        "path": "/test",
        "headers": [(b"Content-Type", b"application/json")],
    }
    receive = mocker.AsyncMock(side_effect=[
        {"type": "http.request", "body": b"Hello", "more_body": True},
        {"type": "http.request", "body": b" World!", "more_body": False},
    ])
    request = Request(scope, receive)

    body = await request.body()
    assert body == b"Hello World!"

@pytest.mark.asyncio
async def test_add_header():
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/test",
        "headers": [(b"Content-Type", b"application/json")],
    }
    receive = lambda: {}
    request = Request(scope, receive)

    request.add_header("Authorization", "Bearer token")
    assert request.headers == {b"Content-Type": b"application/json", b"Authorization": b"Bearer token"}

@pytest.mark.asyncio
async def test_remove_header():
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/test",
        "headers": [(b"Content-Type", b"application/json")],
    }
    receive = lambda: {}
    request = Request(scope, receive)

    request.remove_header("Content-Type")
    assert request.headers == {}

@pytest.mark.asyncio
async def test_set_header():
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/test",
        "headers": [(b"Content-Type", b"application/json")],
    }
    receive = lambda: {}
    request = Request(scope, receive)

    request.set_header("Content-Type", "text/html")
    assert request.headers == {b"Content-Type": b"text/html"}
