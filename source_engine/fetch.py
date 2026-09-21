from __future__ import annotations

import hashlib
import time
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


def _retryable_http_status(status_code: int) -> bool:
    return status_code == 429 or 500 <= status_code <= 599


def fetch(
    url: str,
    timeout: int,
    max_bytes: int,
    user_agent: str,
    retry_attempts: int = 1,
    retry_backoff_seconds: float = 1.0,
) -> FetchResult:
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/json,text/plain;q=0.9,*/*;q=0.1",
    }
    attempts = max(1, int(retry_attempts))
    last_error: requests.RequestException | None = None

    for attempt in range(1, attempts + 1):
        try:
            with requests.get(
                url,
                headers=headers,
                timeout=timeout,
                allow_redirects=True,
                stream=True,
            ) as response:
                if response.status_code >= 400:
                    response.raise_for_status()
                body = b"".join(_bounded_chunks(response, max_bytes))
                return FetchResult(
                    url=response.url,
                    status_code=response.status_code,
                    content_type=response.headers.get("content-type", ""),
                    body=body,
                    sha256=hashlib.sha256(body).hexdigest(),
                    retrieved_at=datetime.now(timezone.utc).isoformat(),
                )
        except requests.HTTPError as exc:
            last_error = exc
            status = getattr(exc.response, "status_code", None)
            if status is not None and not _retryable_http_status(int(status)):
                break
        except (requests.Timeout, requests.ConnectionError) as exc:
            last_error = exc
        except requests.RequestException as exc:
            last_error = exc
            break

        if attempt < attempts:
            time.sleep(max(0.0, float(retry_backoff_seconds)) * attempt)

    assert last_error is not None
    raise FetchError(f"{url}: {last_error}") from last_error
