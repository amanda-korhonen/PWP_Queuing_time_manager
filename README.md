# PWP SPRING 2026
# PROJECT NAME
Queuing Time Manager
# Group information
* Student 1. Amanda Korhonen amanda.korhonen@student.oulu.fi
* Student 2. Leon Piikivi apiikivi21@student.oulu.fi
* Student 3. Teemu Puro tpuro19@student.oulu.fi
* Student 4. Eira Paakkunainen epaakkun21@student.oulu.fi


**Requirements**
* **We recommend using venv**
*  We use SQLite
*  python 3
*  **requirements.txt** file contains all the project dependencies


## How to create database:
We provide db.populate.py to quickly create and populate the database. Use command:
```
python -m queuinghub.db_populate
```

If you want to create and populate manually you can use these code snippets as a quide.

Use line by line in python3 terminal.
To create database:

```
from database import db, Place, Queue, User
from database import app
ctx = app.app_context()
ctx.push()
db.create_all() 
```  

To create a place you can run a code:
```
place1 = Place(name="Bar1", capacity=50, peopleCount=30)
db.session.add(place1)
db.session.commit()
ctx.pop()
```

To add things to an already populated database you have to query the database. Here we have added a queue to an already created **Bar1**:
```
# If you havent run these before then:

from database import db, Place, Queue, User
from database import app
ctx = app.app_context()
ctx.push()

# Continue here if you have run those before in same session:

place1 = Place.query.filter_by(name="Bar1").first()
queue1 = Queue(queue_type="VIP", peopleCount=4, place=place1)
queue2 = Queue(peopleCount=2, place=place1)
db.session.add(queue1) 
db.session.add(queue2) 

# Alternatively
db.session.add_all([queue1, queue2])

# Then commit the changes
db.session.commit()
ctx.pop()
```  
## Deploying API in localhost

To deploy the API for testing in localhost run this command in venv in project root. 
```
flask --app queuinghub run
```
It opens a localhost where you can test the API for example with this URL. 

```
http://127.0.0.1:5000/api/places/
```
URL's that connect to resources:
1. /api/
2. /api/places/
3. /api/places/Place name/
4. /api/places/Place name/queues/
5. /api/places/Place name/queues/Queue type, for example vip/
6. /api/locations/
7. /api/locations/Location name/

Explanations and examples:
1. Returns general information about our API
2. Returns all places in a list that are present in our database

Example:
http://127.0.0.1:5000/api/places/

Returns:
```
[{"name": "Bar1", "capacity": 50, "people_count": 30, "place_type": "Bar", "location": "City1", "fullness": 0.6}, {"name": "Club1", "capacity": 200, "people_count": 120, "place_type": "Club", "location": "City1", "fullness": 0.6}, {"name": "Bar2", "capacity": 100, "people_count": 100, "place_type": "Bar", "location": "City1", "fullness": 1.0}]
```

3. Returns information about certain establishment. 

Example: http://127.0.0.1:5000/api/places/Bar1/

Returns:
```
{"name": "Bar1", "capacity": 50, "people_count": 30, "place_type": "Bar", "location": "City1", "fullness": 0.6}
```
4. Returns all queues that certain establishment has.

Example: http://127.0.0.1:5000/api/places/Club1/queues/

Returns:
```
[{"queue_type": "General", "people_count": 200, "place": "Club1"}, {"queue_type": "VIP", "people_count": 100, "place": "Club1"}]
```
5. Returns certain type of queue from a certain establishment.

Example: http://127.0.0.1:5000/api/places/Club1/queues/VIP/

Returns: 
```
{"queue_type": "VIP", "people_count": 100, "place": "Club1"}
```
6. Returns all places in each location.

Example: http://127.0.0.1:5000/api/locations/

Returns:
```
{"City1": [{"name": "Bar1", "capacity": 50, "people_count": 30, "place_type": "Bar", "location": "City1", "fullness": 0.6}, {"name": "Club1", "capacity": 200, "people_count": 120, "place_type": "Club", "location": "City1", "fullness": 0.6}, {"name": "Bar2", "capacity": 100, "people_count": 100, "place_type": "Bar", "location": "City1", "fullness": 1.0}], "City2": [{"name": "Bar3", "capacity": 50, "people_count": 30, "place_type": "Bar", "location": "City2", "fullness": 0.6}, {"name": "Club2", "capacity": 200, "people_count": 120, "place_type": "Club", "location": "City2", "fullness": 0.6}]}
```

7. Returns all places in certain location.

Example:http://127.0.0.1:5000/api/locations/City2/

Returns:
```
[{"name": "Bar3", "capacity": 50, "people_count": 30, "place_type": "Bar", "location": "City2", "fullness": 0.6}, {"name": "Club2", "capacity": 200, "people_count": 120, "place_type": "Club", "location": "City2", "fullness": 0.6}]
```



## Running tests:  
It is not necessary to create a datbase before testing, the tests create their own temporary databases.  
To get test coverage:  
```
# In project root, run pytest with this command:
pytest --cov-report term-missing --cov=.
```  
This command to run both tests:
```
pytest tests
```  
This command to run database testing:
```
pytest tests/test_db.py 
```  
This command to run resource testing:
```
pytest tests/test_resources.py 
```
To get code quality using PyLint:  
```
pylint queuinghub/* tests
```  








__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint, instructions on how to setup and run the client, instructions on how to setup and run the axiliary service and instructions on how to deploy the api in a production environment__
