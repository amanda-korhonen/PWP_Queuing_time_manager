'''
API file defines these 

This code file is structually taken from this api.py 
with modifications to match our implementation.
https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/blob/ex2-project-layout/sensorhub/api.py

Modification list: variable names, imports.
'''
from flask import Blueprint
from flask_restful import Api  # type: ignore

from .resources.place import PlaceCollection, PlaceItem
from .resources.queue import QueueCollection, QueueItem

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)


def entry():
    '''
    Entry point 

    Added entrypoint from this file:
    https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/blob/ex2-project-layout/sensorhub/views.py

    Modification list: api_name
    '''
    return {"api_version": "1.0", "api_name": "queuing_manager"}

api_bp.add_url_rule("/", "entry", entry)

# NOTE: Vaatii convertterien käyttöä esimerkissä ne oli init tiedostossa
api.add_resource(PlaceCollection, "/places/" )
api.add_resource(PlaceItem, "/places/<place:place>/")
api.add_resource(QueueCollection, "/places/<place:place>/queues/")
api.add_resource(QueueItem, "/places/<place:place>/queues/<string:queue_type>/")
