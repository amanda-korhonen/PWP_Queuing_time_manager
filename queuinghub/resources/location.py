"""
Location Collection and Item classes
This code has the same structure as github Examples provided in Exercise2 of PWP course: 
https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/blob/ex2-project-layout/sensorhub/resources/sensor.py
"""
from collections import defaultdict
from flask_restful import Resource
from werkzeug.exceptions import NotFound

from queuinghub.database import Place

class LocationCollection(Resource):
    """
    LocationCollection is based on this example:

    https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/tree/ex2-project-layout/sensorhub/resources

    Modification list: logic for returning places bu location

    Allowed methods: GET
    """

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
    """
    LocationItem is based on this example:

    https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/tree/ex2-project-layout/sensorhub/resources

    Modification list: variable names.

    Allowed methods: GET
    """

    def get(self, location):
        """
        Get method for LocationItem.
        
        Retuns:
            list: certain location and its' places.
            int: HTTP status code (200)
        
        Exceptions:
            NotFound: If no places exists in a certain location. Flask returns 404. 
        """
        response = []
        places = Place.query.filter_by(location=location).all()
        if not places:
            raise NotFound
        for place in places:
            response.append(place.serialize())
        return response
