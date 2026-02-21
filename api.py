from flask import Blueprint
from flask_restful import Api

from .views import PlaceCollection, PlaceItem, QueueCollection, QueueItem 

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

def entry():
    return {"api_version": "1.0", "api_name": "queuing_manager"}

api_bp.add_url_rule("/", "entry", entry)

# NOTE: Vaatii convertterien käyttöä esimerkissä ne oli init funktiossa
api.add_resourse(PlaceCollection, "/places/" )
api.add_resourse(PlaceItem, "/places/<place:place>/")
api.add_resource(QueueCollection, "/places/<place:place>/queues/")
api.add_resource(QueueItem, "/places/<place:place>/queues/<queue:queue>")
