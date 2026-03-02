from flask import request, Response, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict
from jsonschema import ValidationError, validate
from collections import defaultdict

from queuinghub.database import Place
from queuinghub import db

class LocationCollection(Resource):
    
    def get(self):
        """Get method for LocationCollection."""
        response = []
        places = Place.query.all()
        grouped_places = defaultdict(list)
        for place in places:
            grouped_places[place.location].append(place.serialize())

        return grouped_places, 200
