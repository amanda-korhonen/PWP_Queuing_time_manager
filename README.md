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

**Note!** Please follow this step by step.


## Step 1. How to create database:
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
## Step 2. Deploying API in localhost

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
[
  {
    "name": "Bar1",
    "capacity": 50,
    "people_count": 30,
    "place_type": "Bar",
    "location": "City1",
    "fullness": 0.6
  },
  {
    "name": "Club1",
    "capacity": 200,
    "people_count": 120,
    "place_type": "Club",
    "location": "City1",
    "fullness": 0.6
  },
  {
    "name": "Bar2",
    "capacity": 100,
    "people_count": 100,
    "place_type": "Bar",
    "location": "City1",
    "fullness": 1
  },
  {
    "name": "Bar3",
    "capacity": 50,
    "people_count": 30,
    "place_type": "Bar",
    "location": "City2",
    "fullness": 0.6
  },
  {
    "name": "Club2",
    "capacity": 200,
    "people_count": 120,
    "place_type": "Club",
    "location": "City2",
    "fullness": 0.6
  }
]
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
{
  "City1": [
    {
      "name": "Bar1",
      "URI": "/api/places/Bar1/"
    },
    {
      "name": "Club1",
      "URI": "/api/places/Club1/"
    },
    {
      "name": "Bar2",
      "URI": "/api/places/Bar2/"
    }
  ],
  "City2": [
    {
      "name": "Bar3",
      "URI": "/api/places/Bar3/"
    },
    {
      "name": "Club2",
      "URI": "/api/places/Club2/"
    }
  ]
}
```

7. Returns all places in certain location.

Example:http://127.0.0.1:5000/api/locations/City2/

Returns:
```
[{"name": "Bar3", "URI": "/api/places/Bar3/"}, {"name": "Club2", "URI": "/api/places/Club2/"}]
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


## Deploying Web API

**REQUIRED TOOLS:**
- cPouta login credentials; we used a virtual machine in the cPouta cloud
- VirtualBox with Linux
- venv
- Python
- OpenStack

**SETUP THE ENVIRONMENT:**
1. Start VirtualBox that has Linux.
2. There, inside the VirtualBox Linux, create a separate virtual env to use command-line tools, specifically OpenStack (you can install it in a Python virtual environment). Once the virtual env is created and activated, install tools with the command below:
```
python -m pip install python-openstackclient python-troveclient
```

3. Go to the Pouta dashboard (https://pouta.csc.fi/dashboard/auth/login/?next=/dashboard/). If you haven't logged in already, do it now!

4.  In the dashboard, there is a user menu on the top right. Make sure to download the file that is **tied to your project**.

5.  Now that you have obtained the file in step 4, put it into a suitable location. For example, the bin folder in your virtual environment works well. Now you can source it similarly to how you activate venv itself. For example, if the file's name is _cpouta.sh_ the command is:
```
source /path/to/your/venv/bin/cpouta.sh
```
6.  Before creating your VM, we need to generate an SSH key pair. This is being done so you can get access to your VM after creating it. Do this locally on your own computer using ssh-keygen, and please include a passphrase for your key!
- first, state your (group) name into an environment variable:
```
export PWPGROUP=<group name>
```
- second, run the following command that uses the previously stated environment variable:
```
ssh-keygen -t rsa -f ~/.ssh/$PWPGROUP.key
```

7. Upload the SSH key pair to the cloud. Connect the key only to your own VM whenever you create one. Upload your key with one of them:
- new open stack version:
```
openstack keypair create --public-key ~/.ssh/$PWPGROUP.key.pub $PWPGROUP
```
- older versions:
```
openstack keypair create --from-file ~/.ssh/$PWPGROUP.key.pub $PWPGROUP
```


**DEPLOY WEB API IN THE ENVIRONMENT:**
1. Now that you have created a VM, we will try to connect to it. First, check which floating IP is free using this command:
```
openstack floating ip list
```

2. Look for addresses where _Fixed IP Address_ is _None_. Those addresses are currently not assigned, so you can choose one of them to add to your VM. The command is shown below, and the x.x.x.x is the IP address you are assigning: 
```
openstack server add floating ip $PWPGROUP-vm x.x.x.x
```

3. From now on, use the IP from step 2 to connect to your VM (replace x.x.x.x with it). Please note that your VM will also have a hostname assigned automatically in the form of _fip-x-x-x-x.kaj.poutavm.fi._ 

4. Now you can connect to your VM, for example, with SSH. Connect to your VM as the ubuntu user by adding SSH key to your SSH agent. The commands are the following
```
ssh-add /path/to/your/private/key
ssh ubuntu@x.x.x.x
```
5. You should now see something like _"ubuntu@-vm:~$"_ in the command line if step 4 was successful.


**To run different tests to check that the environment is properly configured, follow these instructions:**

1. 








Ohjeet wikistä: 
A README.md file containing:
List of components that must be installed
How to setup the environment
How to deploy the web api into the environment
How to run the different tests to check that your environment is properly configure








__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint, instructions on how to setup and run the client, instructions on how to setup and run the axiliary service and instructions on how to deploy the api in a production environment__
