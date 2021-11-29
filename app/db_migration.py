# alembic script to initialise a fresh database
# ref: https://alembic.sqlalchemy.org/en/latest/cookbook.html#building-an-up-to-date-database-from-scratch  # NOQA
import logging
from sqlalchemy import create_engine
from alembic.config import Config
from alembic import command

from app.models import Base
from app.config import DATABASE_URL


def create_tables():
    # create any database tables
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)


def stamp_version():
    # stamp latest version
    alembic_cfg = Config("alembic.ini")
    command.stamp(alembic_cfg, "head")


if __name__ == "__main__":
    create_tables()
    stamp_version()
