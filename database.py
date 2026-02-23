from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    people_count = db.Column(db.Integer, nullable=False)
    place_type = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(60), nullable=False)

    queues = db.relationship("Queue", cascade="all, delete-orphan", back_populates = "place")
    user = db.relationship("User", cascade="all, delete-orphan", back_populates = "place")

    '''
    The functions serialize, deserialize and json_schema were created based on the following references:
    - Sensor class of the sensorhub example
    https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/blob/ex2-05-validation/app.py 
    - Chapters Serial Modeling, Embedded Serial Modeling, Deserial Modeling and Dynamic Schemas, Static Methods from course Lovelace 
    https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/implementing-rest-apis-with-flask/#embedded-serial-modeling
    We changed the variable names in the fucntions and the json schema to match our project, but the structure of the functions is based on the references.

    '''

    #A method to change the variables to the correct format to send to the client
    def serialize(self):
        return {
            "name": self.name,
            "capacity": self.capacity,
            "people_count": self.people_count,
            "place_type": self.place_type,
            "location": self.location
        }
    
    #A method to change the variables to the correct format to save to the database
    def deserialize(self, doc):
        self.name = doc["name"]
        self.capacity = doc["capacity"]
        self.people_count = doc["people_count"]
        self.place_type = doc["place_type"]
        self.location = doc["location"]
    
    # the sructure of the json data that the server accepts
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["name", "capacity", "people_count", "place_type", "location"]
        }
        props = schema["properties"] = {}
        props["name"] = {
            "description": "The name of the place",
            "type": "string"
        }
        props["capacity"] = {
            "description": "The maximum capacity of the place",
            "type": "integer"
        }
        props["people_count"] = {
            "description": "The current number of people in the place",
            "type": "integer"
        }
        props["place_type"] = {
            "description": "The type of the place, e.g. restaurant",
            "type": "string"
        }
        props["location"] = {
            "description": "The location of the place",
            "type": "string"
        }
        return schema


class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    queue_type = db.Column(db.String(20), nullable = True)
    people_count = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey("place.id", ondelete="CASCADE"), nullable=False)

    place = db.relationship("Place", back_populates = "queue")

    '''
    The functions serialize, deserialize and json_schema were created based on the following references:
    - Sensor class of the sensorhub example
    https://github.com/UniOulu-Ubicomp-Programming-Courses/pwp-sensorhub-example/blob/ex2-05-validation/app.py 
    - Chapters Serial Modeling, Embedded Serial Modeling, Deserial Modeling and Dynamic Schemas, Static Methods from course Lovelace 
    https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/implementing-rest-apis-with-flask/#embedded-serial-modeling
    We changed the variable names in the fucntions and the json schema to match our project, but the structure of the functions is based on the references.

    '''
    #A method to change the variables to the correct format to send to the client
    def serialize(self):
        return {
            "queue_type": self.queue_type,
            "people_count": self.people_count,
            "place": self.place and self.place.name
        }
    
    #A method to change the variables to the correct format to save to the database
    def deserialize(self, doc):
        self.queue_type = doc["queue_type"]
        self.people_count = doc["people_count"]

    # the sructure of the json data that the server accepts
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["queue_type", "people_count"]
        }
        props = schema["properties"] = {}
        props["queue_type"] = {
            "description": "The type of the queue, e.g. VIP",
            "type": "string"
        }
        props["people"] = {
            "description": "The muber of people in the queue",
            "type": "integer"
        }
        return schema

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), nullable = False)
    place_id = db.Column(db.Integer, db.ForeignKey("place.id", ondelete="CASCADE"), nullable=False)

    place = db.relationship("Place", back_populates = "user")
