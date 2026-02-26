"""Balles"""
import os
import json
import pytest
import random
import tempfile
from flask.testing import FlaskClient
import pytest
from werkzeug.datastructures import Headers

from queuinghub.database import Place, Queue, User
from queuinghub import create_app, db


@pytest.fixture
def client():

    app = create_app(test_config="resourcetest")

    ctx = app.app_context()
    ctx.push()

    db.drop_all()
    db.create_all()
    _populate_db()

    yield app.test_client()

    #db.session.remove()
    #db.drop_all()
    ctx.pop()

def _populate_db():
    """Populates the db with three rows of each table"""
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
        
        u = User(
            password = f"hunter{i}",
            place = p
        )

        db.session.add_all([p, q, u])
    
    db.session.commit()

def _get_place_json():
    """Hardcoded post-ready json for testing"""
    return {"name": "TestPlace",
            "capacity": 300,
            "people_count": 100,
            "place_type": "Nightclub",
            "location": "Turku"
            }

class TestPlaceCollection(object):
    """Tests for the PlaceCollection class"""
    RESOURCE_URL = "/api/places/"

    def test_get(self, client):
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
        valid = _get_place_json()
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201

    def test_headers(self, client):
        valid = _get_place_json()
        valid["name"] = "TestPlace2"
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid["name"] + "/")

    def test_post_wrong_mediatype(self, client):
        valid = _get_place_json()
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

    def test_post_missing_field(self, client):
        valid = _get_place_json()
        valid.pop("location")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

    def test_conflict(self, client):
        valid = _get_place_json()
        valid["name"] = "testingPlace1"
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409


class TestQueueCollection(object):
    
    RESOURCE_URL = "/places/<place:place>/queues/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 3
        for item in body:
            assert "queue_type" in item
            assert "people_count" in item
"""
class TestPlaceItem(object):
    RESOURCE_URL = "/api/places/"
"""