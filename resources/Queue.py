from flask import request, Response, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict
from jsonschema import ValidationError, validate

from database import db, Queue


'''
Queueing Collection and Item classes
'''

class QueueCollection(Resource):

    def get(self):
        response_data =[]
        queues = Queue.query.all()
        for queue in queues:
            response_data.append(queue.serialize())
        return response_data, 200
    
    # NOTE: Mikäli aikaa implementoida admin oikeus
    # @require_adimn
    def post(self, place):
        if not request.json:
            raise UnsupportedMediaType
        
        try:
            validate(request.json, Queue.json_schema())
        except ValidationError as e:
            raise BadRequest(description = str(e))
        
        queue = Queue()
        queue.deserialize(request.json)
        queue.place = place # connects a queue to a certain place
        try:
            db.session.add(queue)
            db.session.commit()
        except IntegrityError:
            raise Conflict(
                description="Place with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(status=201, headers={
            "Location": url_for("api.queueitem", place=place, queue=queue.id)
        })


class QueueItem(Resource):
    def get(self, queue):
        return queue.serialize()

    # NOTE: Mikäli aikaa implementoida admin oikeus
    # @require_adimn
    def put(self, queue):
        if not request.json:
            raise UnsupportedMediaType
        
        try:
            validate(request.json, Queue.json_schema())
        except ValidationError as e:
            raise BadRequest(description = str(e))
        
        queue.deserialize(request.json)
        try:
            db.session.add(queue)
            db.session.commit()
        except IntegrityError:
            raise Conflict(
                description="Place with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(status=204)
    
    # NOTE: Mikäli aikaa implementoida admin oikeus
    # @require_adim
    def delete(self, queue):
        db.session.delete(queue)
        db.session.commit()
        return Response(status=204) # Deleted
