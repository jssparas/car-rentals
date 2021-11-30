import app.config as config
from app.log import get_logger

LOG = get_logger()
result_backend = config.REDIS_URL
broker_url = config.REDIS_URL
redbeat_redis_url = config.REDIS_URL
task_serializer = 'json'
result_serializer = 'json'
# restrict max number of redis connections.
redis_max_connections = 5
broker_pool_limit = None
broker_transport_options = {
    'max_connections': redis_max_connections,
}
# raise an exception if any task goes beyond 2 minutes
task_soft_time_limit = 120
enable_utc = True
timezone = 'UTC'

# # setup periodic jobs
try:
    import app.celery_cron
    beat_schedule = app.celery_cron.beat_schedule
except ImportError:
    LOG.warning('No celery_cron found, check celery_cron_example.py')
