@echo off
call .venv\Scripts\activate
python -m scripts.train
python app.py
