from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone

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
            content = bytearray()
            for chunk in response.iter_content(chunk_size=65536):
                if chunk:
                    content.extend(chunk)
                    if len(content) > max_bytes:
                        raise FetchError(f"response exceeds max_bytes={max_bytes}")
            body = bytes(content)
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
