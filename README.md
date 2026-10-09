# 🎣 Phishing Website Detection — Machine Learning Web App

A complete, beginner-friendly defensive cybersecurity project that detects potentially phishing URLs using machine-learning features extracted from the URL itself.

> **Safety boundary:** This project does **not** visit, crawl, submit forms to, or execute JavaScript on the URL entered by the user. Detection is based only on the text/structure of the URL.

## 1. What this project does

The application accepts a URL such as:

```text
https://secure.example.com/login
```

It extracts lexical and structural indicators, feeds them into a trained `RandomForestClassifier`, and returns:

- predicted class: `PHISHING` or `LEGITIMATE`
- phishing probability
- risk level
- URL features
- human-readable warning signals

The project also includes a REST API, training/evaluation scripts, tests, Docker support, and a small demonstration dataset.

## 2. Architecture

```text
                    ┌──────────────────────────┐
                    │        Browser            │
                    │  URL input + result page │
                    └────────────┬─────────────┘
                                 │ HTTP
                                 ▼
                    ┌──────────────────────────┐
                    │        Flask App         │
                    │  Web UI + REST endpoint  │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │    URL Feature Engine    │
                    │ length, dots, @, IP,     │
                    │ HTTPS, words, entropy…   │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │  Random Forest Classifier │
                    │   trained on demo data   │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Prediction + Explanation │
                    └──────────────────────────┘

Training path:
 demo_urls.csv → feature extraction → train/test split → Random Forest
 → metrics → model/phishing_model.joblib
```

## 3. Technology stack

- Python 3.11–3.13 recommended
- Flask for the web application/API
- pandas for dataset handling
- scikit-learn for the ML model and evaluation
- joblib for model serialization
- pytest for automated tests
- HTML/CSS/JavaScript for the browser UI
- Docker for containerized execution

The project uses Python virtual environments so its packages are isolated from the system Python installation.

## 4. Folder structure

```text
phishing-website-detector/
├── app.py
├── config.py
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
│
├── detector/
│   ├── __init__.py
│   ├── features.py
│   ├── model.py
│   └── utils.py
│
├── data/
│   └── demo_urls.csv
│
├── model/
│   └── .gitkeep
│
├── scripts/
│   ├── __init__.py
│   ├── generate_demo_dataset.py
│   ├── train.py
│   └── evaluate.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── result.html
│
├── static/
│   ├── app.js
│   └── style.css
│
├── tests/
│   ├── __init__.py
│   ├── test_features.py
│   └── test_app.py
│
└── docs/
    ├── PROJECT_REPORT.md
    └── API.md
```

## 5. Step-by-step installation

### Windows PowerShell

```powershell
cd phishing-website-detector
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again.

### Windows CMD

```bat
cd phishing-website-detector
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Linux/macOS

```bash
cd phishing-website-detector
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Optional: generate extra demo data

```bash
python -m scripts.generate_demo_dataset
```

This creates `data/generated_demo_urls.csv`. It is only a teaching aid; it is not a real-world benchmark dataset.

## 7. Train the detector

From the project root:

```bash
python -m scripts.train
```

This creates:

```text
model/phishing_model.joblib
model/metrics.json
```

The training script:

1. loads `data/demo_urls.csv`
2. extracts URL features
3. creates a stratified train/test split
4. trains the Random Forest classifier
5. calculates accuracy, precision, recall, F1, ROC-AUC and a confusion matrix
6. saves the trained model and feature names

## 8. Evaluate the detector

```bash
python -m scripts.evaluate
```

This loads the saved model and evaluates it against the held-out portion recorded by the training pipeline.

## 9. Run the web application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

Paste a URL into the form and click **Analyze URL**.

### API example

```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"url":"https://secure.example.com/login"}'
```

Health check:

```bash
curl http://127.0.0.1:5000/health
```

See `docs/API.md` for the complete API format.

## 10. Run tests

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Then:

```bash
pytest -q
```

## 11. Docker

Build and start the application:

```bash
docker compose up --build
```

Open:

```text
http://127.0.0.1:5000
```

To stop it:

```bash
docker compose down
```

The Docker image trains the model during the image build so the container can start directly.

## 12. How the ML model works

### Input

A URL is treated as a string. The system parses it with Python's standard URL parser and calculates numeric features.

### Important feature groups

| Feature | Meaning |
|---|---|
| `url_length` | Total URL length |
| `hostname_length` | Hostname size |
| `path_length` | Path size |
| `query_length` | Query-string size |
| `num_dots` | Number of `.` characters |
| `num_hyphens` | Number of `-` characters |
| `num_at` | Number of `@` characters |
| `num_digits` | Number of digits |
| `num_slashes` | Number of `/` characters |
| `num_query_marks` | Number of `?` characters |
| `num_equals` | Number of `=` characters |
| `num_ampersands` | Number of `&` characters |
| `num_subdomains` | Approximate hostname subdomain count |
| `has_ip_address` | Whether the hostname looks like an IPv4 address |
| `has_https` | Whether the scheme is HTTPS |
| `has_port` | Whether a non-default port is present |
| `has_punycode` | Whether `xn--` appears in the hostname |
| `suspicious_word_count` | Count of commonly abused phishing terms |
| `digit_ratio` | Fraction of URL characters that are digits |
| `special_char_ratio` | Fraction of non-alphanumeric URL characters |
| `hostname_entropy` | Character-distribution complexity of the hostname |

These signals are intentionally simple and interpretable for a student project. Real production anti-phishing systems normally combine URL intelligence with additional reputation, DNS, certificate, hosting, content, behavioral, and threat-intelligence signals.

## 13. Why Random Forest?

A Random Forest is a practical baseline for this type of tabular feature problem. It can model non-linear combinations of numeric indicators and provides feature-importance values that are useful for a classroom demonstration.

The model in this repository is an educational baseline, **not** a production anti-phishing service.

## 14. Dataset

`data/demo_urls.csv` is a small, hand-curated educational dataset containing examples labeled as legitimate or phishing-like. It exists so the project can run without downloading third-party data.

It is **not** a benchmark-quality dataset and should not be used to claim real-world detection performance.

For a stronger academic experiment, replace it with a reputable phishing/benign URL dataset, document its license/source, remove duplicates, rebalance carefully, and evaluate on a truly unseen test set.

## 15. Important limitations

- The model only sees the URL string; it does not inspect page content.
- Attackers can use legitimate-looking URLs, URL shorteners, compromised domains, or newly registered domains.
- A legitimate URL may contain words that look suspicious.
- Model probabilities are not proof that a URL is malicious.
- Training on a tiny demo dataset can produce misleadingly high test scores.
- This app should not be used as the sole security control.

## 16. Recommended next improvements

1. Train on a large, well-documented real-world dataset.
2. Add a strict deduplication step before splitting data.
3. Add time-based evaluation to test generalization to newer URLs.
4. Compare Random Forest, Logistic Regression, XGBoost/HistGradientBoosting, and calibrated models.
5. Add DNS and domain-age features only in a controlled backend with timeouts and abuse protections.
6. Add threat-intelligence enrichment from trusted services.
7. Add a model registry and versioned datasets.
8. Add rate limiting and authentication before public deployment.
9. Monitor false positives and false negatives.
10. Retrain using newly labeled data and track model drift.

## 17. Academic project flow

Use this sequence for a college/project demonstration:

```text
Problem Definition
       ↓
Data Collection
       ↓
Data Cleaning & Deduplication
       ↓
Feature Engineering
       ↓
Train/Test Split
       ↓
Random Forest Training
       ↓
Model Evaluation
       ↓
Model Serialization
       ↓
Flask Deployment
       ↓
URL Prediction
       ↓
Result + Explainable Signals
```

## 18. Security notes

- Never paste credentials, tokens, session cookies, or private URLs into a public demo.
- The application deliberately does not fetch submitted URLs.
- Keep production deployments behind HTTPS and authentication as appropriate.
- Add input-size limits and rate limiting before exposing the API to the internet.

## 19. References

- Python virtual environments: https://docs.python.org/3/library/venv.html
- Flask documentation: https://flask.palletsprojects.com/
- scikit-learn documentation: https://scikit-learn.org/stable/
- Random Forest classifier: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html

## 20. License

This project is provided for educational and defensive cybersecurity use. See `LICENSE`.
