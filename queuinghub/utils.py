'''
Utility functions and converters.

Whole file taken from:
https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/blob/ex2-project-layout/sensorhub/utils.py
Modifications function names, variable names 

# TODO: Ei oo missään vielä kutsua convertterille
# Tarvitaanko me Queue convertteriä?

'''
from werkzeug.exceptions import NotFound
from werkzeug.routing import BaseConverter

from queuinghub.database import Place, Queue

class PlaceConverter(BaseConverter):
    '''Converter for Place'''
    def to_python(self, value):
        db_place = Place.query.filter_by(name=value).first()
        if db_place is None:
            raise NotFound
        return db_place

    def to_url(self, value):
        return value.name

class QueueConverter(BaseConverter):
    """Converter for Queue"""
    def to_python(self, value):
        db_queue = Queue.query.filter_by(place_id=value).first()
        if db_queue is None:
            raise NotFound
        return db_queue

    def to_url(self, value):
        return value.place_id
