from database import db, Place, Queue, User
from database import app
ctx = app.app_context()
ctx.push()
db.create_all()

place1 = Place(name="Bar1", capacity=50, peopleCount=30)
place2 = Place(name="Club1", capacity=200, peopleCount=120)
place3 = Place(name="Bar2", capacity=100, peopleCount=100)

queue1 = Queue(peopleCount=0, place=place1)
queue2 = Queue(peopleCount=100, place=place2)
queue3 = Queue(peopleCount=50, place=place3)

user1 = User(password="password1", place=place1)
user2 = User(password="password2", place=place2)
user3 = User(password="password3", place=place3)

db.session.add_all([place1, place2, place3, queue1, queue2, queue3, user1, user2, user3])
db.session.commit()
ctx.pop()
