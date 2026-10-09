#!/usr/bin/env bash
set -e
source .venv/bin/activate
python -m scripts.train
python app.py
