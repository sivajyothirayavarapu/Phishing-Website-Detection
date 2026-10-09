# API Reference

## GET /health

Returns the application and model readiness status.

Example response:

```json
{
  "status": "ok",
  "model_ready": true
}
```

## POST /api/predict

Analyze one URL.

Request:

```json
{
  "url": "https://example.com/login"
}
```

Response:

```json
{
  "url": "https://example.com/login",
  "label": "LEGITIMATE",
  "phishing_probability": 0.1234,
  "risk_level": "LOW",
  "signals": [
    "No strong lexical warning signals were triggered by the explanation rules."
  ],
  "features": {
    "url_length": 25
  }
}
```

The `features` object contains the full feature set; the sample above is abbreviated.

## Error codes

- `400`: invalid input
- `413`: request too large
- `503`: model file is not ready

## Security notes

This endpoint does not fetch the provided URL. It only parses and classifies the supplied string.
