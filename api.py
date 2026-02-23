from flask import Blueprint
from flask_restful import Api

from views import PlaceCollection, PlaceItem, QueueCollection, QueueItem 

'''
This code file is structually taken from this file with modifications to match our implementation
https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/blob/ex2-project-layout/sensorhub/api.py
'''

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

def entry():
    return {"api_version": "1.0", "api_name": "queuing_manager"}

api_bp.add_url_rule("/", "entry", entry)

# NOTE: Vaatii convertterien käyttöä esimerkissä ne oli init funktiossa
api.add_resource(PlaceCollection, "/places/" )
api.add_resource(PlaceItem, "/places/<place:place>/")
api.add_resource(QueueCollection, "/places/<place:place>/queues/")
api.add_resource(QueueItem, "/places/<place:place>/queues/<queue:queue>")
