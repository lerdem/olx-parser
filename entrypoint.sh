#!/bin/sh
python -m ad.upload_ads &
python -m ad.bulk_deactivation_inactive_ads &
gunicorn --threads 4 --bind 0.0.0.0:8000 app:app
