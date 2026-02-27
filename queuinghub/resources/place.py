'''
Place Collection and Item classes
This code has the same structure as github Examples provided in Exercise2 of PWP course: 
https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/blob/ex2-project-layout/sensorhub/resources/sensor.py

#TODO fullness apufunktio tänne tai jonnekki muualle
'''
from flask import request, Response, url_for
from flask_restful import Resource # pylint: disable=import-error
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict
from jsonschema import ValidationError, validate # pylint: disable=import-error

from queuinghub.database import db, Place

class PlaceCollection(Resource):
    """
    PlaceCollection is based on these examples:

    https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/tree/ex2-project-layout/sensorhub/resources

    And POST implementation from this excersice:
    https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/implementing-rest-apis-with-flask/#posting-it-all-together

    Modification list: variable names.

    Allowed methods: GET, POST
    """
    def get(self):
        """Get method for PlaceCollection."""
        response = []
        places = Place.query.all()
        for place in places:
            response.append(place.serialize())
        return response, 200

    def post(self):
        """Post method for PlaceCollection."""
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(request.json, Place.json_schema())
        except ValidationError as e:
            raise BadRequest(description = str(e)) from e

        place = Place()
        place.deserialize(request.json)
        try:
            db.session.add(place)
            db.session.commit()
        except IntegrityError as e:
            raise Conflict(
                description=f"Place with name {place.name} already exists."
            ) from e
        return Response(status=201, headers= {
            "Location": url_for("api.placeitem", place=place)
        })

class PlaceItem(Resource):
    """
    PlaceItem is based on these examples:

    https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/tree/ex2-project-layout/sensorhub/resources

    And POST implementation from this excersice.
    https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/implementing-rest-apis-with-flask/#posting-it-all-together

    Modification list: variable names.

    Allowed methods: GET, PUT, DELETE
    """
    def get(self, place):
        """Get method for a specific place."""
        return {
            "name": place.name,
            "capacity": place.capacity,
            "people_count": place.people_count,
            "place_type": place.place_type,
            "location": place.location
        }

    # NOTE: Mikäli aikaa implementoida admin oikeus
    # @require_adimn
    # NOTE: Itemille oma schema?
    def put(self, place):
        """Put method for place."""
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, Place.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        place.deserialize(request.json)

        try:
            db.session.add(place)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback() # Use rollback because of unique constraint
            raise Conflict(
                description=f"Place with name {place.name} already exists."
            ) from e
        return Response(status=201, headers= {
            "Location": url_for("api.placeitem", place=place)
        })

    # NOTE: Mikäli aikaa implementoida admin oikeus
    # @require_admin
    def delete(self, place):
        """Delete method for place."""
        db.session.delete(place)
        db.session.commit()
        return Response(status=204) # Deleted
