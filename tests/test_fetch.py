from __future__ import annotations

import requests

from source_engine import fetch


class _Response:
    url = "https://example.com/"
    status_code = 200
    headers = {"content-type": "text/plain"}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def raise_for_status(self):
        return None

    def iter_content(self, chunk_size=65536):
        yield b"example.com\n"


def test_fetch_retries_transient_request_error(monkeypatch):
    calls = {"count": 0}

    def fake_get(*args, **kwargs):
        calls["count"] += 1
        if calls["count"] == 1:
            raise requests.Timeout("temporary timeout")
        return _Response()

    monkeypatch.setattr(fetch.requests, "get", fake_get)
    monkeypatch.setattr(fetch.time, "sleep", lambda _: None)

    result = fetch.fetch(
        "https://example.com/",
        timeout=45,
        max_bytes=1024,
        user_agent="test",
        retry_attempts=2,
        retry_backoff_seconds=0,
    )

    assert calls["count"] == 2
    assert result.body == b"example.com\n"


def test_fetch_keeps_fail_closed_after_retry_budget(monkeypatch):
    calls = {"count": 0}

    def fake_get(*args, **kwargs):
        calls["count"] += 1
        raise requests.Timeout("persistent timeout")

    monkeypatch.setattr(fetch.requests, "get", fake_get)
    monkeypatch.setattr(fetch.time, "sleep", lambda _: None)

    try:
        fetch.fetch(
            "https://example.com/",
            timeout=45,
            max_bytes=1024,
            user_agent="test",
            retry_attempts=2,
            retry_backoff_seconds=0,
        )
    except fetch.FetchError as exc:
        assert "persistent timeout" in str(exc)
    else:
        raise AssertionError("persistent timeout must remain a FetchError")

    assert calls["count"] == 2


class _ForbiddenResponse(_Response):
    status_code = 403

    def raise_for_status(self):
        raise requests.HTTPError(response=self)


def test_fetch_does_not_retry_non_transient_4xx(monkeypatch):
    calls = {"count": 0}

    def fake_get(*args, **kwargs):
        calls["count"] += 1
        return _ForbiddenResponse()

    monkeypatch.setattr(fetch.requests, "get", fake_get)
    monkeypatch.setattr(fetch.time, "sleep", lambda _: None)

    try:
        fetch.fetch(
            "https://example.com/",
            timeout=45,
            max_bytes=1024,
            user_agent="test",
            retry_attempts=3,
            retry_backoff_seconds=0,
        )
    except fetch.FetchError:
        pass
    else:
        raise AssertionError("403 must fail without retry")
    assert calls["count"] == 1
