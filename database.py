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
    peopleCount = db.Column(db.Integer, nullable=False)

    queue = db.relationship("Queue", back_populates = "place")
    user = db.relationship("User", back_populates = "place")


class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    queue_type = db.Column(db.String(20), nullable = True)
    peopleCount = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey("place.id"))

    place = db.relationship("Place", back_populates = "queue")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), nullable = False)
    place_id = db.Column(db.Integer, db.ForeignKey("place.id"))

    place = db.relationship("Place", back_populates = "user")
