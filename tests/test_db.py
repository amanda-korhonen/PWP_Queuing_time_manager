'''Testing for the database models.'''
import os
import tempfile
import pytest
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError

from queuinghub.database import Place, Queue, User # pylint: disable=import-error
from queuinghub import create_app, db # pylint: disable=import-error

'''
The tests in this file are based on the example test file provided in the course materials:
https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/blob/ex2-project-layout/tests/test_db.py
The variables and functions have been changed to fit our project and our models, 
but the structure is from the example.
'''

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    '''Enable foreign key support for SQLite.'''
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@pytest.fixture
def db_handle():
    '''Setting up a temporary database for testing.'''
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

def _get_place(name="Test Place", capacity=10, place_type="Test Type", location="Test Location"):
    '''Helper function to create a Place instance.'''
    place = Place(
        name=name,
        capacity=capacity,
        people_count=0,
        place_type=place_type,
        location=location
    )
    return place

def _get_queue(name="Test Queue"):
    '''Helper function to create a Queue instance.'''
    queue = Queue(
        name=name,
        people_count=0
    )
    return queue

def _get_user(password="testpassword"):
    '''Helper function to create a User instance.'''
    user = User(
        password=password
    )
    return user

def test_create_instances(db_handle):
    '''Tests creating instances of Place, Queue, and User.'''

    #creation
    place = _get_place()
    queue = _get_queue()
    user = _get_user()
    #relationships
    queue.place = place
    place.queues.append(queue)
    user.place = place

    db_handle.session.add(place)
    db_handle.session.add(queue)
    db_handle.session.add(user)
    db_handle.session.commit()

    #check that the created instances exist
    assert place.query.count() == 1
    assert queue.query.count() == 1
    assert user.query.count() == 1
    db_place = place.query.first()
    db_queue = queue.query.first()
    db_user = user.query.first()

    #check relationships
    assert db_queue.place == db_place
    assert db_user.place == db_place
    assert db_queue in db_place.queues

def test_place_one_to_many_queue(db_handle):
    '''Tests that we can add more than one queue to a place.'''
    place = _get_place()
    queue1 = _get_queue(name="Queue 1")
    queue2 = _get_queue(name="Queue 2")

    queue1.place = place
    queue2.place = place

    db_handle.session.add(place)
    db_handle.session.add(queue1)
    db_handle.session.add(queue2)
    db_handle.session.commit()

    db_place = place.query.first()
    assert len(db_place.queues) == 2

def test_user_onetoone_place(db_handle):
    '''Tests that a user can be associated with only one place.'''
    place1 = _get_place(name="Place 1")
    place2 = _get_place(name="Place 2")
    user = _get_user()

    user.place = place1

    db_handle.session.add(place1)
    db_handle.session.add(place2)
    db_handle.session.add(user)
    db_handle.session.commit()

    # Try to associate the same user with another place, should raise an error
    with pytest.raises(IntegrityError):
        #user.place = place2
        db_handle.session.commit()

def test_queue_ondelete_place(db_handle):
    '''Tests that deleting a place also deletes its queues.'''
    place = _get_place()
    queue = _get_queue()

    queue.place = place

    db_handle.session.add(place)
    db_handle.session.add(queue)
    db_handle.session.commit()

    db_handle.session.delete(place)
    db_handle.session.commit()

    assert place.query.count() == 0
    assert queue.query.count() == 0

def test_queue_columns(db_handle):
    '''Tests that the columns accept the expected values. Numerical columns accept only numbers,
    and string columns accept only strings.'''
    queue = _get_queue()

    queue.queue_type = 1  # Invalid type, should raise an error
    db_handle.session.add(queue)
    with pytest.raises(StatementError):
        db_handle.session.commit()

    db_handle.session.rollback()  # Rollback the failed transaction

    queue = _get_queue()
    queue.people_count = "Not a number"  # Invalid type, should raise an error
    db_handle.session.add(queue)
    with pytest.raises(StatementError):
        db_handle.session.commit()

    db_handle.session.rollback()

    queue = _get_queue()
    queue.queue_type = None  # A needed variable, should raise an error
    db_handle.session.add(queue)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

    db_handle.session.rollback()

    queue = _get_queue()
    queue.people_count = None  # A needed variable, should raise an error
    db_handle.session.add(queue)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

def test_place_columns(db_handle):
    '''Tests that the columns accept the expected values.'''
    place = _get_place()

    place.name = 123  # Invalid type, should raise an error
    db_handle.session.add(place)
    with pytest.raises(StatementError):
        db_handle.session.commit()

    db_handle.session.rollback()

    place = _get_place()
    place.capacity = "Not a number"  # Invalid type, should raise an error
    db_handle.session.add(place)
    with pytest.raises(StatementError):
        db_handle.session.commit()

    db_handle.session.rollback()

    place = _get_place()
    place.people_count = "Not a number"  # Invalid type, should raise an error
    db_handle.session.add(place)
    with pytest.raises(StatementError):
        db_handle.session.commit()

    db_handle.session.rollback()

    place = _get_place()
    place.place_type = 456  # Invalid type, should raise an error
    db_handle.session.add(place)
    with pytest.raises(StatementError):
        db_handle.session.commit()

    db_handle.session.rollback()

    place = _get_place()
    place.location = 789  # Invalid type, should raise an error
    db_handle.session.add(place)
    with pytest.raises(StatementError):
        db_handle.session.commit()

    db_handle.session.rollback()

    place = _get_place()
    place.name = None  # A needed variable, should raise an error
    db_handle.session.add(place)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

    db_handle.session.rollback()

    place = _get_place()
    place.capacity = None  # A needed variable, should raise an error
    db_handle.session.add(place)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

    db_handle.session.rollback()

    place = _get_place()
    place.people_count = None  # A needed variable, should raise an error
    db_handle.session.add(place)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

    db_handle.session.rollback()

    place = _get_place()
    place.place_type = None  # A needed variable, should raise an error
    db_handle.session.add(place)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

    db_handle.session.rollback()

    place = _get_place()
    place.location = None  # A needed variable, should raise an error
    db_handle.session.add(place)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()


def test_queue_unique_constraint(db_handle):
    '''Tests that the queue name is unique within a place.'''
    queue1 = _get_queue(name="Queue 1")
    queue2 = _get_queue(name="Queue 1")  # Same name to trigger unique constraint

    db_handle.session.add(queue1)
    db_handle.session.add(queue2)

    with pytest.raises(IntegrityError):
        db_handle.session.commit()
