from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, render_template, request

from config import DEBUG, HOST, MAX_URL_LENGTH, MODEL_PATH, PORT
from detector.features import explain_url
from detector.model import PhishingModel
from detector.utils import normalize_input, safe_url_preview

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

_model: PhishingModel | None = None


def get_model() -> PhishingModel:
    global _model
    if _model is None:
        if not Path(MODEL_PATH).exists():
            raise RuntimeError(
                f"Model file not found at {MODEL_PATH}. Run 'python -m scripts.train' first."
            )
        _model = PhishingModel.load(MODEL_PATH)
    return _model


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    model_ready = Path(MODEL_PATH).exists()
    return jsonify({"status": "ok", "model_ready": model_ready})


@app.post("/api/predict")
def api_predict():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "")
    if not isinstance(url, str):
        return jsonify({"error": "url must be a string"}), 400
    if len(url) > MAX_URL_LENGTH:
        return jsonify({"error": "URL exceeds the 4096-character limit"}), 400

    try:
        normalized = normalize_input(url)
        result = get_model().predict(normalized)
        result["url"] = safe_url_preview(normalized)
        result["signals"] = explain_url(normalized)
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 503


@app.post("/predict")
def form_predict():
    url = request.form.get("url", "")
    try:
        normalized = normalize_input(url)
        result = get_model().predict(normalized)
        result["url"] = safe_url_preview(normalized)
        result["signals"] = explain_url(normalized)
        return render_template("result.html", result=result)
    except (ValueError, RuntimeError) as exc:
        return render_template("result.html", error=str(exc), result=None), 400


@app.errorhandler(413)
def too_large(_error):
    return jsonify({"error": "Request body is too large."}), 413


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
