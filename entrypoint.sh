#!/bin/sh
python -m ad.adapters.repository
python -m ad.upload_ads &
python -m ad.telegram_sender &
gunicorn --threads 4 --bind 0.0.0.0:8000 app:app
