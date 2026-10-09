from __future__ import annotations

import json
from pathlib import Path

from config import MODEL_PATH


def main() -> None:
    metrics_path = Path(MODEL_PATH).with_name("metrics.json")
    if not metrics_path.exists():
        raise SystemExit("No metrics.json found. Run: python -m scripts.train")

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    print("Saved evaluation metrics")
    print("=" * 30)
    for key, value in metrics.items():
        print(f"{key:>16}: {value}")


if __name__ == "__main__":
    main()
