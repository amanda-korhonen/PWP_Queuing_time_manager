'''
Utility functions and converters.

Whole file taken from:
https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/blob/ex2-project-layout/sensorhub/utils.py
Modifications function names, variable names

'''
from werkzeug.exceptions import NotFound
from werkzeug.routing import BaseConverter

from queuinghub.database import Place

class PlaceConverter(BaseConverter):
    '''Converter for Place'''
    def to_python(self, value):
        '''
        Converts a URL path component into a database object.

        Args:
            value (string): The place name we got from the URL.

        Returns:
            The place object that matches this given name.

        Exceptions:
            NotFound: If there is no such place name. Flask returns 404. 
        '''
        db_place = Place.query.filter_by(name=value).first()
        if db_place is None:
            raise NotFound
        return db_place

    def to_url(self, value):
        '''
        Converts a place database object into a string for URL generation.

        Args: 
            value (Place): The place object that is converted to URL string.

        Returns: 
            string: The name of the place, used when constructing URL 
        '''
        return value.name
