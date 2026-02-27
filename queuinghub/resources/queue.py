"""
Queueing Collection and Item classes
"""

from flask import request, Response, url_for
from flask_restful import Resource  # pylint: disable=import-error
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict
from jsonschema import ValidationError, validate # pylint: disable=import-error

from queuinghub.database import db, Queue

class QueueCollection(Resource):
    """
    QueueCollection is based on these examples:

    https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/tree/ex2-project-layout/sensorhub/resources

    And POST implementation from this excersice:
    https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/implementing-rest-apis-with-flask/#posting-it-all-together

    Modification list: variable names.

    Allowed methods: GET, POST
    """

    def get(self, place):
        """Get method for all queues in place."""
        response_data = []
        queues = Queue.query.filter_by(place=place).all()
        for queue in queues:
            response_data.append(queue.serialize())
        return response_data, 200

    # NOTE: Mikäli aikaa implementoida admin oikeus
    # @require_adimn
    def post(self, place):
        """Post method for a queue."""
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(request.json, Queue.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        queue = Queue()
        queue.deserialize(request.json)
        queue.place = place  # connects a queue to a certain place
        print(queue)
        try:
            db.session.add(queue)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback() # Use rollback because of unique constraint
            raise Conflict(
                description=f"Queue type {queue.queue_type} already exists in {place.name}."
            ) from e
        return Response(
            status=201,
            headers={"Location": url_for("api.queueitem", place=place, queue=queue)},
        )


class QueueItem(Resource):
    """
    QueueItem is based on these examples:

    https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/tree/ex2-project-layout/sensorhub/resources

    And POST implementation from this excersice.
    https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/implementing-rest-apis-with-flask/#posting-it-all-together

    Modification list: variable names.

    Allowed methods: GET, PUT, DELETE
    """

    def get(self, queue, place):
        """Get method for a specific queue"""
        return {
            "queue_type": queue.queue_type,
            "people_count": queue.people_count,
            "place": place.name
        }

    # NOTE: Mikäli aikaa implementoida admin oikeus
    # @require_adimn
    def put(self, queue, place):
        """Put method for a specific queue"""
        if not request.json:
            raise UnsupportedMediaType

        try:
            validate(request.json, Queue.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        queue.deserialize(request.json)
        try:
            db.session.add(queue)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback() # Use rollback because of unique constraint
            raise Conflict(
                description=f"Queue type {queue.queue_type} already exists in {place.name}."
            ) from e
        return Response(
            status=201,
            headers={"Location": url_for("api.queueitem", place=place, queue=queue)},
        )

    # NOTE: Mikäli aikaa implementoida admin oikeus
    # @require_adim
    def delete(self, queue):
        """Delete for queue"""
        db.session.delete(queue)
        db.session.commit()
        return Response(status=204)  # Deleted
