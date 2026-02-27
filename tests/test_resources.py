"""
Testing module for API resources.
Most of this code is the same as in exercise 2 github:
https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/blob/ex2-project-layout/tests/test_resource.py

Tests are mostly 1:1 as in the exercise, but the test setup is slightly different.
Instead of using tempfiles, the test fixture makes a test database in the instance folder.
This allows for easier debugging (in my opinion).
"""
import json
import pytest

from queuinghub.database import Place, Queue, User
from queuinghub import create_app, db


@pytest.fixture(name="client")
def fixture_client():
    """
    Initialize app and database. Fixture found from following post to keep pylint from screaming:
    https://stackoverflow.com/questions/46089480/pytest-fixtures-redefining-name-from-outer-scope-pylint
    """

    app = create_app(test_config="resourcetest")

    ctx = app.app_context()
    ctx.push()

    db.drop_all()
    db.create_all()
    _populate_db()

    yield app.test_client()
    # Following commands empty the database after testing if wanted
    #db.session.remove()
    #db.drop_all()

    ctx.pop()

def _populate_db():
    """Populates the db with three rows of each table, except for Queue (6 tables)."""
    for i in range(1, 4):
        p = Place(
            name = f"testingPlace{i}",
            capacity = 200,
            people_count = 50,
            place_type = "TestPlace",
            location = "TestLocation"
        )

        q = Queue(
            queue_type = f"testQueue{i}",
            people_count = i + 5,
            place = p
        )

        q2 = Queue(
            queue_type = f"extraTestQueue{i}",
            people_count = i + 6,
            place = p
        )

        u = User(
            password = f"hunter{i}",
            place = p
        )

        db.session.add_all([p, q, q2, u])

    db.session.commit()

def _get_place_json():
    """Hardcoded POST/PUT-ready json for Place tests."""
    return {"name": "TestPlace",
            "capacity": 300,
            "people_count": 100,
            "place_type": "Nightclub",
            "location": "Turku"
            }

def _get_queue_json():
    """Hardcoded POST/PUT-ready json for Queue tests."""
    return {"queue_type": "VIP",
            "people_count": 30
            }

class TestPlaceCollection():
    """Tests for the PlaceCollection class."""

    RESOURCE_URL = "/api/places/"

    def test_get(self, client):
        """Test for GET request."""
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 3 #Three rows in db during testing
        for item in body:
            assert "name" in item
            assert "capacity" in item
            assert "people_count" in item
            assert "place_type" in item
            assert "location" in item

    def test_post_valid_request(self, client):
        """Test for valid POST request."""
        valid = _get_place_json()
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201

    def test_headers(self, client):
        """Test for headers."""
        valid = _get_place_json()
        valid["name"] = "TestPlace2"
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid["name"] + "/")

    def test_post_wrong_mediatype(self, client):
        """Test for wrong mediatype."""
        valid = _get_place_json()
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

    def test_post_missing_field(self, client):
        """Test for missing field in JSON."""
        valid = _get_place_json()
        valid.pop("location")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

    def test_conflict(self, client):
        """Test for conflict (already exists)."""
        valid = _get_place_json()
        valid["name"] = "testingPlace1"
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

    def test_not_allowed(self, client):
        """Test for non-supported method."""
        valid = _get_place_json()
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 405


class TestQueueCollection():
    """Tests for the QueueCollection class."""

    RESOURCE_URL = "/api/places/testingPlace1/queues/"

    def test_get(self, client):
        """Test for GET request."""
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 2 # Two rows of queues per place in testing
        for item in body:
            assert "queue_type" in item
            assert "people_count" in item

    def test_post_valid_request(self, client):
        """Test for valid POST request."""
        valid = _get_queue_json()
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201

    def test_headers(self, client):
        """Test for headers."""
        valid = _get_queue_json()
        valid["queue_type"] = "Ticketless"
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid["queue_type"] + "/")

    def test_post_wrong_mediatype(self, client):
        """Test for wrong mediatype."""
        valid = _get_queue_json()
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

    def test_post_missing_field(self, client):
        """Test for missing field in JSON."""
        valid = _get_queue_json()
        valid.pop("queue_type")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

    def test_conflict(self, client):
        """Test for conflict (already exists)."""
        valid = _get_queue_json()
        valid["queue_type"] = "testQueue1"
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

    def test_not_allowed(self, client):
        """Test for non-supported method."""
        valid = _get_queue_json()
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 405


class TestPlaceItem():
    """Tests for the PlaceItem class."""

    RESOURCE_URL = "/api/places/testingPlace1/"
    INVALID_URL = "/api/places/noTestingPlace/"

    def test_get(self, client):
        """Test for GET request."""
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 5 # Five attributes in one place
        assert "name" in body
        assert "capacity" in body
        assert "people_count" in body
        assert "place_type" in body
        assert "location" in body

    def test_not_found(self, client):
        """Test for invalid URL."""
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put_valid_request(self, client):
        """Test for valid PUT request."""
        valid = _get_place_json()
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201

    def test_headers(self, client):
        """Test for headers."""
        valid = _get_place_json()
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.headers["Location"].endswith(valid["name"] + "/")

    def test_put_wrong_mediatype(self, client):
        """Test for wrong mediatype."""
        valid = _get_place_json()
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

    def test_put_missing_field(self, client):
        """Test for missing field in JSON."""
        valid = _get_place_json()
        valid.pop("name")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

    def test_put_conflict(self, client):
        """Test for conflict (already exists)."""
        valid = _get_place_json()
        valid["name"] = "testingPlace3"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

    def test_delete(self, client):
        """Test for DELETE request."""
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204

    def test_not_allowed(self, client):
        """Test for non-supported method."""
        valid = _get_place_json()
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 405

class TestQueueItem():
    """Tests for the QueueItem class."""

    RESOURCE_URL = "/api/places/testingPlace1/queues/testQueue1/"
    INVALID_URL = "/api/places/testingPlace1/queues/noTestQueue/"

    def test_get(self, client):
        """Test for GET request."""
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 3 # Three attributes in one Queue
        assert "queue_type" in body
        assert "people_count" in body
        assert "place" in body

    def test_not_found(self, client):
        """Test for invalid URL."""
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put_valid_request(self, client):
        """Test for valid PUT request."""
        valid = _get_queue_json()
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201

    def test_headers(self, client):
        """Test for headers."""
        valid = _get_queue_json()
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.headers["Location"].endswith(valid["queue_type"] + "/")

    def test_put_wrong_mediatype(self, client):
        """Test for wrong mediatype."""
        valid = _get_queue_json()
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

    def test_put_missing_field(self, client):
        """Test for missing field in JSON."""
        valid = _get_queue_json()
        valid.pop("queue_type")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

    def test_put_conflict(self, client):
        """Test for conflict (already exists)."""
        valid = _get_queue_json()
        valid["queue_type"] = "extraTestQueue1"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

    def test_delete(self, client):
        """Test for DELETE request."""
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204

    def test_not_allowed(self, client):
        """Test for non-supported method."""
        valid = _get_queue_json()
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 405
