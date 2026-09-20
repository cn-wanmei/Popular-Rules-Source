from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterator

import requests


@dataclass(frozen=True)
class FetchResult:
    url: str
    status_code: int
    content_type: str
    body: bytes
    sha256: str
    retrieved_at: str


class FetchError(RuntimeError):
    pass


def _bounded_chunks(response: requests.Response, max_bytes: int) -> Iterator[bytes]:
    total = 0
    for chunk in response.iter_content(chunk_size=65536):
        if not chunk:
            continue
        total += len(chunk)
        if total > max_bytes:
            raise FetchError(f"response exceeds max_bytes={max_bytes}")
        yield chunk


def fetch(url: str, timeout: int, max_bytes: int, user_agent: str) -> FetchResult:
    now = datetime.now(timezone.utc).isoformat()
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/json,text/plain;q=0.9,*/*;q=0.1",
    }
    try:
        with requests.get(
            url,
            headers=headers,
            timeout=timeout,
            allow_redirects=True,
            stream=True,
        ) as response:
            response.raise_for_status()
            body = b"".join(_bounded_chunks(response, max_bytes))
            return FetchResult(
                url=response.url,
                status_code=response.status_code,
                content_type=response.headers.get("content-type", ""),
                body=body,
                sha256=hashlib.sha256(body).hexdigest(),
                retrieved_at=now,
            )
    except requests.RequestException as exc:
        raise FetchError(f"{url}: {exc}") from exc
