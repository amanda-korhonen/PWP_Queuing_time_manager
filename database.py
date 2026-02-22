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

    '''
    def serialize(self):
        return {
            "queue_type": self.queue_type,
            "people_count": self.people_count,
            "place": self.place and self.place.name
        }
    
    def deserialize(self, doc):
        self.queue_type = doc["queue_type"]
        self.people_count = doc["people_count"]

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
