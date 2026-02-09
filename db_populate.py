from database import db, Place, Queue, User
from database import app
ctx = app.app_context()
ctx.push()
db.create_all()

place1 = Place(name="Bar1", capacity=50, peopleCount=30)
place2 = Place(name="Club1", capacity=200, peopleCount=120)
place3 = Place(name="Bar2", capacity=100, peopleCount=100)

queue1 = Queue(queue_type="entry", peopleCount=0, place=place1)
queue2 = Queue(queue_type="entry", peopleCount=100, place=place2)
queue3 = Queue(queue_type="entry", peopleCount=50, place=place3)

db.session.add_all([place1, place2, place3, queue1, queue2, queue3])
db.session.commit()
ctx.pop()
