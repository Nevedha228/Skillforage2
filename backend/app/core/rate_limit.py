"""Simple in-memory rate limiter for auth endpoints (no extra dependency)."""
from collections import defaultdict
from datetime import datetime, timedelta
from fastapi import HTTPException, Request, status

_hits: dict[str, list[datetime]] = defaultdict(list)


def enforce_rate_limit(request: Request, key_suffix: str, max_hits: int = 8, window_seconds: int = 60) -> None:
    ip = request.client.host if request.client else "unknown"
    key = f"{ip}:{key_suffix}"
    now = datetime.utcnow()
    cutoff = now - timedelta(seconds=window_seconds)
    recent = [t for t in _hits[key] if t > cutoff]
    if len(recent) >= max_hits:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please wait a minute and try again.",
        )
    recent.append(now)
    _hits[key] = recent
