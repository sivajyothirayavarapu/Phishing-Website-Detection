from __future__ import annotations

import csv
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "generated_demo_urls.csv"

BENIGN_DOMAINS = [
    "example.com", "example.org", "example.net", "docs.example.com",
    "portal.example.org", "shop.example.com", "news.example.net",
]
PHISH_TEMPLATES = [
    "http://{brand}-verify.example.test/login",
    "http://{brand}-security.example.test/confirm",
    "http://{brand}-account.example.test/update?verify=true",
    "http://secure-{brand}.example.test/password/reset",
    "http://urgent-{brand}.example.test/payment/confirm",
]
BRANDS = ["account", "paypal", "microsoft", "apple", "google", "amazon", "netflix"]


def main() -> None:
    rows: list[tuple[str, int]] = []
    for domain in BENIGN_DOMAINS:
        for path in ["/", "/login", "/support", "/products", "/docs/start"]:
            rows.append((f"https://{domain}{path}", 0))
    for brand in BRANDS:
        for template in PHISH_TEMPLATES:
            rows.append((template.format(brand=brand), 1))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["url", "label"])
        writer.writerows(rows)
    print(f"Wrote {len(rows)} demo rows to {OUT}")


if __name__ == "__main__":
    main()
