"""Balles"""
import os
import json
import pytest
import random
import tempfile
#from queuinghub.db_populate import populate_database
from flask.testing import FlaskClient
import pytest
from werkzeug.datastructures import Headers

from queuinghub import create_app, db


@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()

    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True,
        "CACHE_TYPE": "SimpleCache",
    }

    app = create_app(config)

    ctx = app.app_context()
    ctx.push()

    db.create_all()

    yield app.test_client()

def _get_place_json():
    return {"name": "TestPlace",
            "capacity": 300,
            "people_count": 100,
            "place_type": "Nightclub",
            "location": "Turku"
            }

class TestPlaceCollection(object):
    
    RESOURCE_URL = "/api/places/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 0
        for item in body:
            assert "name" in item
            assert "capacity" in item
            assert "people_count" in item
            assert "place_type" in item
            assert "location" in item

    def test_post_valid_request(self, client):
        valid = _get_place_json()
        print(valid)
        resp = client.post(self.RESOURCE_URL)
        assert resp.status_code == 201
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid["name"] + "/")
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["name"] == "Restaurant1"
        assert body[""]

    def test_post_wrong_mediatype(self, client):
        valid = _get_place_json()
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415

    def test_post_missing_field(self, client):
        valid = _get_place_json()
        valid.pop("location")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code(400)

    def test_conflict(self, client):
        valid = _get_place_json()
        valid["name"] = "Bar1"
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

class TestQueueCollection(object):
    
    RESOURCE_URL = ""

    def test_get(self, client):
        resp = client.get(self)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 3
        for item in body:
            assert "queue_type" in item
            assert "people_count" in item

class TestPlaceItem(object):
    RESOURCE_URL = "/api/places/"