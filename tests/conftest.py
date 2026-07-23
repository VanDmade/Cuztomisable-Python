import os
import uuid

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SQLASession, sessionmaker

from cuztomisable import Cuztomisable
from cuztomisable.db.models.users.user import User
from cuztomisable.helpers.dependencies import configure_db, get_db
from cuztomisable.helpers.security import hash_password

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "Set DATABASE_URL to run the test suite, e.g.\n"
        "  DATABASE_URL=postgresql+psycopg://user:pass@localhost/dbname pytest"
    )

_engine = create_engine(DATABASE_URL)

# Used by things that grab a session outside of FastAPI's DI (e.g. the global
# exception handler's error logging) — a plain sessionmaker on the real
# engine, same as how the consuming app wires this up in production.
configure_db(sessionmaker(bind=_engine))


@pytest.fixture()
def db():
    """Wraps each test in a transaction (using a savepoint so the app's own
    db.commit() calls don't end it early) that's rolled back afterward, so
    tests never leave data behind in the real database."""
    connection = _engine.connect()
    transaction = connection.begin()
    session = SQLASession(bind=connection, join_transaction_mode="create_savepoint")

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def app(db):
    fastapi_app = FastAPI()
    Cuztomisable(fastapi_app)
    fastapi_app.dependency_overrides[get_db] = lambda: (yield db)
    return fastapi_app


@pytest.fixture()
def client(app):
    # application.py's exception handler is registered for the bare
    # Exception class, which Starlette attaches to ServerErrorMiddleware —
    # that middleware re-raises the original exception after sending the
    # response, for every error it handles, not just genuine 500s. Without
    # raise_server_exceptions=False, TestClient would re-raise expected,
    # already-handled 400s (e.g. "invalid code") instead of just returning
    # the response.
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture()
def user(db):
    record = User(
        name="Test User",
        username=f"testuser_{uuid.uuid4().hex[:8]}",
        email=f"test-{uuid.uuid4().hex[:8]}@example.com",
        password=hash_password("Sup3rSecret!123"),
    )
    db.add(record)
    db.flush()
    return record
