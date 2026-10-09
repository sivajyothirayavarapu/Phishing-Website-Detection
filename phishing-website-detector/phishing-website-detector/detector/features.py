from __future__ import annotations

import ipaddress
import math
import re
from collections import Counter
from urllib.parse import urlparse

FEATURE_NAMES = [
    "url_length",
    "hostname_length",
    "path_length",
    "query_length",
    "fragment_length",
    "num_dots",
    "num_hyphens",
    "num_at",
    "num_digits",
    "num_slashes",
    "num_query_marks",
    "num_equals",
    "num_ampersands",
    "num_percent",
    "num_subdomains",
    "has_ip_address",
    "has_https",
    "has_port",
    "has_punycode",
    "has_double_slash_path",
    "suspicious_word_count",
    "brand_word_count",
    "digit_ratio",
    "special_char_ratio",
    "hostname_entropy",
    "path_entropy",
]

SUSPICIOUS_WORDS = {
    "account",
    "authenticate",
    "authentication",
    "billing",
    "confirm",
    "confirmation",
    "credential",
    "gift",
    "invoice",
    "login",
    "mfa",
    "password",
    "payment",
    "recover",
    "reset",
    "secure",
    "security",
    "signin",
    "support",
    "unlock",
    "update",
    "urgent",
    "verify",
    "verification",
    "wallet",
}

BRAND_WORDS = {
    "apple",
    "amazon",
    "google",
    "microsoft",
    "paypal",
    "facebook",
    "instagram",
    "linkedin",
    "netflix",
    "docusign",
    "dropbox",
    "github",
}


def _tokenize(url: str) -> list[str]:
    return [token for token in re.split(r"[^a-z0-9]+", url.lower()) if token]


def _is_ipv4(hostname: str) -> int:
    if not hostname:
        return 0
    try:
        return int(isinstance(ipaddress.ip_address(hostname), ipaddress.IPv4Address))
    except ValueError:
        return 0


def _entropy(value: str) -> float:
    if not value:
        return 0.0
    counts = Counter(value)
    length = len(value)
    return -sum((count / length) * math.log2(count / length) for count in counts.values())


def _safe_parse(url: str):
    candidate = url.strip()
    if not candidate:
        return urlparse("")
    if "://" not in candidate:
        candidate = "http://" + candidate
    return urlparse(candidate)


def extract_features(url: str) -> dict[str, float]:
    """Extract URL-only lexical features. No network request is performed."""
    url = str(url or "").strip()
    parsed = _safe_parse(url)
    hostname = (parsed.hostname or "").lower()
    path = parsed.path or ""
    query = parsed.query or ""
    fragment = parsed.fragment or ""
    tokens = _tokenize(url)

    digits = sum(ch.isdigit() for ch in url)
    special = sum(not ch.isalnum() for ch in url)
    labels = [part for part in hostname.split(".") if part]
    subdomains = max(0, len(labels) - 2)

    suspicious_word_count = sum(token in SUSPICIOUS_WORDS for token in tokens)
    brand_word_count = sum(token in BRAND_WORDS for token in tokens)
    try:
        port = parsed.port
    except ValueError:
        port = None

    return {
        "url_length": float(len(url)),
        "hostname_length": float(len(hostname)),
        "path_length": float(len(path)),
        "query_length": float(len(query)),
        "fragment_length": float(len(fragment)),
        "num_dots": float(url.count(".")),
        "num_hyphens": float(url.count("-")),
        "num_at": float(url.count("@")),
        "num_digits": float(digits),
        "num_slashes": float(url.count("/")),
        "num_query_marks": float(url.count("?")),
        "num_equals": float(url.count("=")),
        "num_ampersands": float(url.count("&")),
        "num_percent": float(url.count("%")),
        "num_subdomains": float(subdomains),
        "has_ip_address": float(_is_ipv4(hostname)),
        "has_https": float(parsed.scheme.lower() == "https"),
        "has_port": float(port is not None and port not in {80, 443}),
        "has_punycode": float("xn--" in hostname),
        "has_double_slash_path": float("//" in path),
        "suspicious_word_count": float(suspicious_word_count),
        "brand_word_count": float(brand_word_count),
        "digit_ratio": float(digits / len(url)) if url else 0.0,
        "special_char_ratio": float(special / len(url)) if url else 0.0,
        "hostname_entropy": float(_entropy(hostname)),
        "path_entropy": float(_entropy(path)),
    }


def explain_url(url: str) -> list[str]:
    """Create simple human-readable rule signals alongside the ML prediction."""
    f = extract_features(url)
    signals: list[str] = []

    if f["has_ip_address"]:
        signals.append("The hostname is an IPv4 address rather than a normal domain name.")
    if f["num_at"]:
        signals.append("The URL contains @, which can be abused to make a URL look trustworthy.")
    if f["has_punycode"]:
        signals.append("The hostname contains punycode (xn--), which deserves extra review.")
    if f["num_subdomains"] >= 3:
        signals.append("The hostname contains several subdomain levels.")
    if f["url_length"] > 100:
        signals.append("The URL is unusually long.")
    if f["suspicious_word_count"] >= 2:
        signals.append("The URL contains multiple security/account/payment themed words.")
    elif f["suspicious_word_count"] == 1:
        signals.append("The URL contains a security/account/payment themed word.")
    if f["brand_word_count"]:
        signals.append("A well-known brand name appears in the URL; verify the actual registrable domain.")
    if f["digit_ratio"] > 0.20:
        signals.append("The URL contains a relatively high proportion of digits.")
    if f["has_port"]:
        signals.append("A non-default network port is present.")
    if f["num_percent"] >= 4:
        signals.append("The URL uses substantial percent-encoding.")
    if f["has_double_slash_path"]:
        signals.append("The path contains a double slash.")

    if not signals:
        signals.append("No strong lexical warning signals were triggered by the explanation rules.")
    return signals


def feature_vector(url: str) -> list[float]:
    features = extract_features(url)
    return [features[name] for name in FEATURE_NAMES]
