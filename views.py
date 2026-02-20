from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType
from database import db, Place

class PlaceCollection(Resource):
    
    def get(self):
        response = []
        places = Place.query.all()
        for place in places:
            response.append([place.name, 
                            place.capacity, 
                            place.people_count, 
                            place.place_type, 
                            place.location])
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
        except KeyError:
            return 400
        except IntegrityError:
            return 400

        return "Success", 201
            

class PlaceItem(Resource):
    
    def get(self, place):
        return {
            "name": place.name,
            "capacity": place.capacity,
            "people_count": place.people_count,
            "place_type": place.place_type,
            "location": place.location
        }
    
    def delete(self, place):
        db.session.delete(place)
        db.session.commit()
        return "Deleted", 204
