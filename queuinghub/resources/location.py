"""Docstring placeholder"""
from collections import defaultdict
from flask_restful import Resource
from werkzeug.exceptions import NotFound

from queuinghub.database import Place

class LocationCollection(Resource):
    """Docstring placeholder."""

    def get(self):
        """
        Get method for LocationCollection.
        
        Retuns:
            dictionary: all locations and corresponding places.
            int: HTTP status code (200)
        """
        places = Place.query.all()
        grouped_places = defaultdict(list)
        for place in places:
            grouped_places[place.location].append(place.serialize())
        return grouped_places, 200

class LocationItem(Resource):
    """Docstring placeholder."""

    def get(self, location):
        """
        Get method for LocationItem.
        
        Retuns:
            dictionary: certain location and its' places.
            int: HTTP status code (200)
        
        Exceptions:
            NotFound: If no places excists in certain location. Flask returns 404. 
        """
        response = []
        places = Place.query.filter_by(location=location).all()
        if not places:
            raise NotFound
        for place in places:
            response.append(place.serialize())
        return response
