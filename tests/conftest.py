import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app.config.celery import celery
from app.config.db import Base

pytest_plugins = ("celery.contrib.pytest",)


@pytest.fixture(scope="session")
def db_engine(request):
    engine = create_engine("postgresql+psycopg://pytest:pytest@localhost:5432/pytest")
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)
        engine.dispose()

    request.addfinalizer(teardown)
    return engine


@pytest.fixture(scope="session")
def db_session_factory(db_engine):
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope="function", autouse=True)
def db_session(db_session_factory, request):
    session = db_session_factory()

    def teardown():
        session.rollback()
        session.close()

    request.addfinalizer(teardown)

    return session


@pytest.fixture(scope="module")
def celery_app(request):
    celery.conf.update(CELERY_ALWAYS_EAGER=True)
    return celery
