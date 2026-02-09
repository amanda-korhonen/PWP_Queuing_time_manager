# PWP SPRING 2026
# PROJECT NAME
Queuing Time Manager
# Group information
* Student 1. Amanda Korhonen amanda.korhonen@student.oulu.fi
* Student 2. Leon Piikivi apiikivi21@student.oulu.fi
* Student 3. Teemu Puro tpuro19@student.oulu.fi
* Student 4. Eira Paakkunainen epaakkun21@student.oulu.fi


__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint, instructions on how to setup and run the client, instructions on how to setup and run the axiliary service and instructions on how to deploy the api in a production environment__

**Requirements**
* We recommend using venv when creating and populating database.
*  We used SQLite and requirements.txt file contains all the project dependencies. 
* We use python 3


__How to create database:__
We provide db.populate.py to quickly create and populate the database. If you want to create and populate manually you can use these code snippets as a quide.

Use line by line in python3 terminal.
To create database:

```
from database import db, Place, Queue, User
from database import app
ctx = app.app_context()
ctx.push()
db.create_all()
```  


To add things to an already populated database you have to query the database. Here we have added a queue to Bar1:
```
from database import db, Place, Queue, User
from database import app
ctx = app.app_context()
ctx.push()
place1 = Place.query.filter_by(name="Bar1").first()
queue2 = Queue(queue_type="VIP", peopleCount=4, place=place1)
db.session.add(queue2)
db.session.commit()
ctx.pop()
```
