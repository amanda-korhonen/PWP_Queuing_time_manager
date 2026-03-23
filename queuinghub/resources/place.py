'''
Place Collection and Item classes
This code has the same structure as github Examples provided in Exercise2 of PWP course: 
https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/blob/ex2-project-layout/sensorhub/resources/sensor.py

#TODO fullness apufunktio tänne tai jonnekki muualle
'''
import os
from flask import request, Response, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict
from jsonschema import ValidationError, validate
from flasgger import swag_from

from queuinghub.database import Place
from queuinghub import cache, db

#path for /queuinghub
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#path for /queuinghub/doc
DOCS_DIR = os.path.join(BASE_DIR, "doc")

class PlaceCollection(Resource):
    """
    PlaceCollection is based on these examples:

    https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/tree/ex2-project-layout/sensorhub/resources

    And POST implementation from this excersice:
    https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/implementing-rest-apis-with-flask/#posting-it-all-together

    Modification list: variable names.

    Allowed methods: GET, POST
    """
    @cache.cached(timeout=30, response_filter=lambda r: False)
    @swag_from(os.path.join(DOCS_DIR, "placecollection/get.yml"))
    def get(self):
        """
        Get method for PlaceCollection.
        
        Returns:
            list: a list of serialized Places
            int: HTTP status code (200)
        """
        response_data = []
        places = Place.query.all()
        for place in places:
            response_data.append(place.serialize())
        return response_data, 200

    @swag_from(os.path.join(DOCS_DIR, "placecollection/post.yml"))
    def post(self):
        """
        Post method for PlaceCollection.
        
        Returns:
            Response: HTTP status code: 201, and url for new Place

        Exceptions:
            UnsupportedMediaType: If the request is not json.
            BadRequest: If JSON schema validation does not pass.
            Conflict: If there is already place with that name.
        """
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
    @swag_from(os.path.join(DOCS_DIR, "placeitem/get.yml"))
    def get(self, place):
        """
        Get method for a specific place.
        
        Args: 
            place (Place): the place object from database, name from converter.

        Returns:
            dictionary: serialized place object

        """
        return place.serialize()

    # NOTE: Mikäli aikaa implementoida admin oikeus
    # @require_adimn
    # NOTE: Itemille oma schema?
    @swag_from(os.path.join(DOCS_DIR, "placeitem/put.yml"))
    def put(self, place):
        """
        Put method for place.

        Args:
            place (Place): Place object that we update with put.
        
        Returns:
            Response: HTTP status code: 201, and url for the updated Place

        Exceptions:
            UnsupportedMediaType: If the request is not json.
            BadRequest: If JSON schema validation does not pass.
            Conflict: If the put tries to rename the place to a name 
                that already excists. -> Rolls back the session.
        """
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
    @swag_from(os.path.join(DOCS_DIR, "placeitem/delete.yml"))
    def delete(self, place):
        """
        Delete method for place.
        
        Args:
            place (Place): Place object that we want to delete.

        Returns: 
            Response: HTTP status code: 204 
        """
        db.session.delete(place)
        db.session.commit()
        return Response(status=204) # Deleted
