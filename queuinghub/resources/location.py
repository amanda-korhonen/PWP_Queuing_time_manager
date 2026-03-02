"""Docstring placeholder"""
from collections import defaultdict
from flask_restful import Resource
from werkzeug.exceptions import NotFound

from queuinghub.database import Place

class LocationCollection(Resource):
    """Docstring placeholder."""

    def get(self):
        """Get method for LocationCollection."""
        places = Place.query.all()
        grouped_places = defaultdict(list)
        for place in places:
            grouped_places[place.location].append(place.serialize())
        return grouped_places, 200

class LocationItem(Resource):
    """Docstring placeholder."""

    def get(self, location):
        """Get method for LocationItem."""
        response = []
        places = Place.query.filter_by(location=location).all()
        if not places:
            raise NotFound
        for place in places:
            response.append(place.serialize())
        return response
