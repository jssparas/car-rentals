# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from app.models import Base
from app import config
from app.log import get_logger
LOG = get_logger()


def get_engine(uri):
    LOG.info('Connecting to database...')
    options = {
        'pool_recycle': 3600,
        'pool_size': 5,
        'pool_timeout': 45,
        'max_overflow': 20,
    }
    return create_engine(uri, **options)


db_session = scoped_session(sessionmaker())
engine = get_engine(config.DATABASE_URL)


def init_session():
    db_session.configure(bind=engine)
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        LOG.error('Database initialisation failed...', exc_info=True)
        raise


# redis session
# rdb = redis.Redis.from_url(config.REDIS_URL)
