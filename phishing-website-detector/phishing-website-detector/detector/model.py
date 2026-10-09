from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

from .features import FEATURE_NAMES, feature_vector


class PhishingModel:
    """Train, save, load, and predict with the phishing classifier."""

    def __init__(self, estimator: RandomForestClassifier | None = None):
        self.estimator = estimator or RandomForestClassifier(
            n_estimators=300,
            max_depth=None,
            min_samples_leaf=1,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        )

    @classmethod
    def load(cls, path: str | Path) -> "PhishingModel":
        payload = joblib.load(path)
        model = cls(payload["model"])
        model.feature_names = payload.get("feature_names", FEATURE_NAMES)
        return model

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(
            {"model": self.estimator, "feature_names": FEATURE_NAMES},
            path,
        )

    def train_from_dataframe(self, df: pd.DataFrame) -> dict[str, Any]:
        required = {"url", "label"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        df = df.dropna(subset=["url", "label"]).drop_duplicates(subset=["url"]).copy()
        X = np.asarray([feature_vector(url) for url in df["url"]], dtype=float)
        y = df["label"].astype(int).to_numpy()

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.25,
            random_state=42,
            stratify=y,
        )

        self.estimator.fit(X_train, y_train)
        pred = self.estimator.predict(X_test)
        proba = self.estimator.predict_proba(X_test)[:, 1]

        metrics = {
            "samples": int(len(df)),
            "train_samples": int(len(X_train)),
            "test_samples": int(len(X_test)),
            "accuracy": round(float(accuracy_score(y_test, pred)), 4),
            "precision": round(float(precision_score(y_test, pred, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, pred, zero_division=0)), 4),
            "f1": round(float(f1_score(y_test, pred, zero_division=0)), 4),
            "roc_auc": round(float(roc_auc_score(y_test, proba)), 4),
        }
        return metrics

    def predict(self, url: str) -> dict[str, Any]:
        vector = np.asarray([feature_vector(url)], dtype=float)
        predicted = int(self.estimator.predict(vector)[0])
        probability = float(self.estimator.predict_proba(vector)[0, 1])
        label = "PHISHING" if predicted == 1 else "LEGITIMATE"

        if probability >= 0.75:
            risk = "HIGH"
        elif probability >= 0.45:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        features = dict(zip(FEATURE_NAMES, vector[0].tolist()))
        return {
            "label": label,
            "phishing_probability": round(probability, 4),
            "risk_level": risk,
            "features": features,
        }


def save_metrics(metrics: dict[str, Any], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
