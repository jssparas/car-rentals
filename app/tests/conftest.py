# conftest.py - common, shared pytest fixtures
# ref: https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions  # NOQA


from falcon import testing
import pytest
from sqlalchemy.orm import sessionmaker, scoped_session
from app.models import Base
from app.config import DATABASE_URL
from app.database import get_engine
from app.utils import seed
from app import log
LOG = log.get_logger()


# test client fixture
@pytest.fixture(scope='session')
def client(request):
    """ Client app instance """
    from app.main import app
    yield testing.TestClient(app)


# db fixtures
# ref: https://gist.github.com/tribals/2eb07d1bafefc2a6695671a171a8e6b1
@pytest.fixture(scope="module")
def engine():
    engine = get_engine(DATABASE_URL)
    yield engine


@pytest.fixture(scope='function', autouse=True)
def db(engine):
    """ DB instance """
    LOG.info("Setting up db...")
    session = scoped_session(sessionmaker(bind=engine))
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    seed(engine)

    yield session

    session.close()
    session.remove()
    session.rollback()
