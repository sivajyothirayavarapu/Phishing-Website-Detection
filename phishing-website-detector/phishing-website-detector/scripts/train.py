from __future__ import annotations

from pathlib import Path

import pandas as pd

from config import DATA_PATH, MODEL_PATH
from detector.model import PhishingModel, save_metrics


PROJECT_ROOT = Path(__file__).resolve().parents[1]
METRICS_PATH = PROJECT_ROOT / "model" / "metrics.json"


def main() -> None:
    print(f"[+] Loading dataset: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    print(f"[+] Rows before cleaning: {len(df)}")

    model = PhishingModel()
    metrics = model.train_from_dataframe(df)
    model.save(MODEL_PATH)
    save_metrics(metrics, METRICS_PATH)

    print("[+] Training complete")
    print(f"[+] Model: {MODEL_PATH}")
    print(f"[+] Metrics: {METRICS_PATH}")
    for key, value in metrics.items():
        print(f"    {key}: {value}")


if __name__ == "__main__":
    main()
