from functools import wraps
import json
import secrets
from flask import request
from werkzeug.exceptions import Forbidden, NotFound
from werkzeug.routing import BaseConverter

from .database import Place
'''
TODO: Ei oo missään vielä kutsua convertterille
Tarvitaanko me Queue convertteriä?
'''

class PlaceConverter(BaseConverter):
    
    def to_python(self, place_name):
        db_place = Place.query.filter_by(name=place_name).first()
        if db_place is None:
            raise NotFound
        return db_place

    def to_url(self, db_place):
        return db_place.name




