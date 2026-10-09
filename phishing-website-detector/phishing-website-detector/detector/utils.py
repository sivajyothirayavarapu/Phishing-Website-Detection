from __future__ import annotations

import re
from urllib.parse import urlparse


def normalize_input(url: str) -> str:
    value = str(url or "").strip()
    if not value:
        raise ValueError("URL cannot be empty.")
    if len(value) > 4096:
        raise ValueError("URL is too long. Maximum allowed length is 4096 characters.")
    parsed = urlparse(value if "://" in value else f"http://{value}")
    if not parsed.netloc:
        raise ValueError("Please enter a valid URL or domain, such as https://example.com")
    return value


def safe_url_preview(url: str) -> str:
    return re.sub(r"\s+", " ", url).strip()
