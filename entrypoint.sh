#!/bin/sh
(
  while true; do
    python -m ad.upload_ads
    # Random sleep between 60 and 120 seconds in shell
    SLEEP_TIME=$((60 + RANDOM % 61))
    echo "UPLOADER: sleeping for ${SLEEP_TIME}s"
    sleep $SLEEP_TIME
  done
) &
python -m ad.bulk_deactivation_inactive_ads &
exec gunicorn --threads 4 --bind 0.0.0.0:8000 app:app
