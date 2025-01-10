import pytest
from typing import List, Tuple
from krieg.core.headers import Header

def test_initialize_empty_headers():
    header = Header()
    assert header.get_headers() == []
    assert header.get_header("Content-Type") is None

def test_initialize_with_headers():
    headers = [(b"Content-Type", b"application/json"), (b"Authorization", b"Bearer token")]
    header = Header(headers)
    assert header.get_headers() == [(b"Content-Type", b"application/json"), (b"Authorization", b"Bearer token")]
    assert header.get_header("Content-Type") == b"application/json"
    assert header.get_header("Authorization") == b"Bearer token"

def test_add_header():
    header = Header()
    header.add_header("Content-Type", "application/json")
    assert header.get_headers() == [(b"Content-Type", b"application/json")]
    assert header.get_header("Content-Type") == b"application/json"

def test_add_header_empty_name():
    header = Header()
    with pytest.raises(ValueError):
        header.add_header("", "application/json")

def test_add_header_empty_value():
    header = Header()
    with pytest.raises(ValueError):
        header.add_header("Content-Type", "")

def test_remove_header():
    header = Header()
    header.add_header("Content-Type", "application/json")
    header.remove_header("Content-Type")
    assert header.get_headers() == []
    assert header.get_header("Content-Type") is None

def test_set_header():
    header = Header()
    header.set_header("Content-Type", "application/json")
    assert header.get_headers() == [(b"Content-Type", b"application/json")]
    assert header.get_header("Content-Type") == b"application/json"

    header.set_header("Content-Type", "text/html")
    assert header.get_headers() == [(b"Content-Type", b"text/html")]
    assert header.get_header("Content-Type") == b"text/html"

def test_get_header_non_existent():
    header = Header()
    assert header.get_header("Non-Existent-Header") is None
