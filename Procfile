web: gunicorn --reload app.main:app -b 0.0.0.0:8000
worker: celery worker --app=app.celery:celery_app --loglevel=DEBUG -n worker@%h
cron: celery beat -S redbeat.RedBeatScheduler --app=app.celery:celery_app --loglevel=DEBUG