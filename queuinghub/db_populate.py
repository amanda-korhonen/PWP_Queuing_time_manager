"""Module for populating database."""
from queuinghub.database import db, Place, Queue, User
ctx = app.app_context()
ctx.push()
db.create_all()

place1 = Place(name="Bar1", capacity=50, peopleCount=30, place_type="Bar", location="City1")
place2 = Place(name="Club1", capacity=200, peopleCount=120, place_type="Club", location="City1")
place3 = Place(name="Bar2", capacity=100, peopleCount=100, place_type="Bar", location="City1")

queue1 = Queue(queue_type="General", peopleCount=0, place=place1)
queue2 = Queue(queue_type="VIP", peopleCount=100, place=place2)
queue3 = Queue(peopleCount=50, place=place3)

user1 = User(password="password1", place=place1)
user2 = User(password="password2", place=place2)
user3 = User(password="password3", place=place3)

db.session.add_all([place1, place2, place3, queue1, queue2, queue3, user1, user2, user3])
db.session.commit()
ctx.pop()
