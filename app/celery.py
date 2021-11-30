import os

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, scoped_session
from celery import Task, Celery
from celery.signals import worker_init, task_prerun

from app.log import get_logger
from app import celery_config
from app.database import engine


LOG = get_logger()

included_modules = ['app.tasks']
celery_app = Celery(include=included_modules)
celery_app.config_from_object(celery_config)

# create sqlalchemy db session, once for a worker
# ref: http://stackoverflow.com/a/17224993
wdb_session = scoped_session(sessionmaker())


@worker_init.connect
def initialize_session(signal=None, sender=None, **kwargs):
    LOG.info('initialising worker wdb_session (sender=%s)', sender)
    wdb_session.configure(bind=engine)


@task_prerun.connect
def on_task_init(*args, **kwargs):
    LOG.debug('Cleaning up db connections')
    engine.dispose()


# define DBTask for tasks which need sqlalchemy session access
class DBTask(Task):
    """
    An abstract Celery Task that ensures that the connection to the
    database is closed on task completion.
    ref http://www.prschmid.com/2013/04/using-sqlalchemy-with-celery-tasks.html
    """
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        wdb_session.remove()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        if wdb_session is not None:
            if isinstance(exc, SQLAlchemyError):
                wdb_session.rollback()
            wdb_session.remove()


# ref: http://docs.celeryproject.org/en/latest/getting-started/next-steps.html#project-layout  # NOQA
if __name__ == '__main__':
    celery_app.start()
