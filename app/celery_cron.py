from celery.schedules import crontab

beat_schedule = {
    'update-car-available-date': {
        'task': 'app.tasks.update_available_dates',
        'schedule': crontab(day_of_week='*', hour='00', minute='15'),
        # 'schedule': 60.0        # for testing cron
    },
}
