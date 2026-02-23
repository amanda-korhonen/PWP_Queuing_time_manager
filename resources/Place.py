from flask import request, Response, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict
from jsonschema import ValidationError, validate

from database import db, Place

'''
Place Collection and Item classes

#TODO fullness apufunktio tänne tai jonnekki muualle
'''
class PlaceCollection(Resource):
    
    def get(self):
        response = []
        places = Place.query.all()
        for place in places:
            response.append(place.serialize())
        return response, 200
    
    def post(self):
        if not request.json:
            raise UnsupportedMediaType

        # Placeholder for schema-validation
        try:
            place = Place(
                name=request.json["name"],
                capacity=request.json["capacity"],
                people_count=request.json["people_count"],
                place_type=request.json["place_type"],
                location=request.json["location"]
            )

            db.session.add(place)
            db.session.commit()
        except KeyError as e:
            raise BadRequest(description = str(e))
        except IntegrityError:
            raise Conflict(
                description="Place with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(status=201, headers= {
            "Location": url_for("api.placeitem", place=place)
        })
            
class PlaceItem(Resource):
    
    def get(self, place):
        return {
            "name": place.name,
            "capacity": place.capacity,
            "people_count": place.people_count,
            "place_type": place.place_type,
            "location": place.location
        }
    
    # NOTE: Mikäli aikaa implementoida admin oikeus
    # @require_adimn
    def put(self, place):
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, Place.json_schema())
        except ValidationError  as e:
            raise BadRequest(description=str(e))
        
        place.deserialize(request.json)

        try:
            db.session.add(place)
            db.session.commit()
        except IntegrityError:
            raise Conflict(
                description="Place with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(status=204)
        
    # NOTE: Mikäli aikaa implementoida admin oikeus
    # @require_adimn
    def delete(self, place):
        db.session.delete(place)
        db.session.commit()
        return Response(status=204) # Deleted

