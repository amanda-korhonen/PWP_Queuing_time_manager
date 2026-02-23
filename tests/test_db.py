import os
import pytest
import tempfile
from sqlalchemy.engine import Engine
from sqlalchemy import event 

from queuinghub import create_app, database
from queuinghub.database import Place, Queue, User

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@pytest.fixture
def db_handle():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }

    app = create_app(config)

    ctx = app.app_context()
    ctx.push()
    db.create_all()

    yield db

    db.session.rollback()
    db.drop_all()
    db.session.remove()
    ctx.pop()
    os.close(db_fd)
    os.unlink(db_fname)