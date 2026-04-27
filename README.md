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

To create database run in project root:

```
flask --app=queuinghub init-db
```

### Older instructions 
Use line by line in python3 terminal.
To create database:
```
from queuinghub.database import db, Place, Queue, User
from queuinghub import create_app, db
app = create_app()
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

## Test Client
To get client code quality using ESLint:
```
npm run lint
```


## Deploying Web API

### **REQUIRED TOOLS:**
- CSC cloud service: cPouta login credentials; we used a virtual machine in the cPouta cloud
- VirtualBox with Linux
- venv
- Python
- OpenStack
- Ubuntu (use _standard.small_)
- gunicorn
- nginx
- supervisor
- SSH
- Git
- Flask

### **SETUP THE ENVIRONMENT**

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

### **GENERATE AN SSH KEY PAIR**

Before creating your VM, we need to generate an SSH key pair. This is being done so you can get access to your VM after creating it. Do this locally on your own computer using ssh-keygen, and please include a passphrase for your key!

1.  State your (group) name into an environment variable:
```
export PWPGROUP=<group name>
```

2. Run the following command that uses the previously stated environment variable:
```
ssh-keygen -t rsa -f ~/.ssh/$PWPGROUP.key
```

3. Upload the SSH key pair to the cloud. Connect the key only to your own VM whenever you create one. Upload your key with:
```
#new open stack version:
openstack keypair create --public-key ~/.ssh/$PWPGROUP.key.pub $PWPGROUP

#older versions:
openstack keypair create --from-file ~/.ssh/$PWPGROUP.key.pub $PWPGROUP
```

### **CREATE A VM**

Now we are actually creating the VM itself. For this, use the **latest Ubuntu image** and choose _**standard.small**_. The command below assumes that you are using the previously stated Ubuntu image and _standard.small_.

1. Create a VM using the previously stated Ubunty image:
```
openstack server create --flavor standard.small --image Ubuntu-24.04 --key-name $PWPGROUP $PWPGROUP-vm
```
2. Attach a security group that allows SSH into your server:
```
openstack server add security group $PWPGROUP-vm ssh
```
**HOX!** In this case, the necessary security groups are pre-created for the course, so there is no need to create them.

3. Add one more security group so that HTTP(S) connections to your server can be accepted:
```
openstack server add security group $PWPGROUP-vm web
```

### **CONNECT TO YOUR VM**
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


### **DEPLOY WEB API IN THE ENVIRONMENT**

In this step, we assume that you are working inside a VM owned by the login user. The current working directory must be the virtual environment's root.

You can follow the instructions below, or alternatively, you can run the following setup script:


1. Clone the project to your desired directory:
```
git clone https://github.com/amanda-korhonen/PWP_Queuing_time_manager.git
```
2. Navigate to misc directory:
```
cd /path/to/project/misc
```
3. Run the setup script:
```
sudo sh full_setup.sh
```
Running this script streamlines the deployment, only thing left is to edit the nginx configuration file found with:
```
sudo nano /etc/nginx/sites-enabled/queuinghub
```
Where host_name should be changed to the address/domain name where the API is hosted from e.g. <127.0.0.1> or <place.holder.com>.

4. (Optional) Setting up the client to nginx, run:
```
sudo sh client_setup.sh
```
This command will setup the client in our repo to be hosted in nginx.
Please note that you will need to change the address in the api.js -file (as the setup instructs)
There are posted instructions for applying for a certificate for advanced users, but currently it might take some extra tinkering, since certbot modifies the nginx conf file quite liberally. 

### **FULL SETUP INSTRUCTIONS BEGIN HERE:**

1. Start prepping inside the VM
```
sudo apt update
sudo apt install -y python3 python3-pip python3.12-venv git nginx
python3 -m venv venv
source venv/bin/activate
```

2. Download the project, install it and do the basic setup:
```
git clone https://github.com/amanda-korhonen/PWP_Queuing_time_manager.git queuinghub
```
**Note!** In Linux virtual environments, the Flask instance folder is located in _/path/to/your/venv/var/sensorhub-instance_ by default.

3. Move to the folder where the project is
```
cd PWP_Queuing_time_manager
```

4. Install project requirements
```
pip install -r requirements.txt
```

5. Install Gunicorn
```
pip install "gunicorn<25"
```

6. Initialize database
```
flask --app=sensorhub init-db
```

7. Create a system user and switch into it
```
sudo useradd --system hub
exec su -p $USER
```

8. Create the hub folder and grant ownership to hub user, drop all privileges from other users
```
sudo mkdir /opt/hub
sudo chown hub:hub /opt/hub
sudo chmod -R o-rwx /opt/hub
```

9. Create venv for the new hub user
```
sudo apt install python3.12-venv
sudo -u hub python3 -m venv /opt/hub/venv
```

10. Clone the project for the user
```
sudo -u hub git clone https://github.com/amanda-korhonen/PWP_Queuing_time_manager.git queuinghub /opt/hub/hub
```

11. Move to the hub folder where the hub-user project is
```
cd /opt/hub/hub
```

12. Create the postactive file
```
sudo -u hub touch /opt/hub/venv/bin/postactivate
```

13. Make an environment variable. This is being put in the postactivate file
```
echo 'export GUNICORN_WORKERS=3' | sudo tee -a /opt/hub/venv/bin/postactivate
```

14. Activate environments and add environment variables
```
source /opt/hub/venv/bin/activate
source /opt/hub/venv/bin/postactivate
```

15. Install project requirements for the hub user's project
```
sudo -u hub -E env PATH=$PATH python -m pip install -r requirements.txt
```

16. Set up a database for the hub user's project
```
sudo -u hub -E env PATH=$PATH flask --app=queuinghub init-db
```

17. Install for the hub user and run Gunicorn as the hub user
```
python -m pip install "gunicorn<25"
sudo -u hub -E env PATH=$PATH gunicorn -w $GUNICORN_WORKERS "hub:create_app()"
```

18. Make a directory for scripts
```
sudo -u hub mkdir /opt/hub/venv/scripts
```

19. Create a script that starts the gunicorn
```
sudo -u hub touch /opt/hub/venv/scripts/start_gunicorn
```

20. Execute rights
```
sudo chmod u+x /opt/hub/venv/scripts/start_gunicorn
```

21. Enter to edit the start_gunicorn script
```
sudo -u hub nano /opt/hub/venv/scripts/start_gunicorn
```
and make it look like this:
```
#!/bin/sh

cd /opt/hub/hub
. /opt/hub/venv/bin/activate
. /opt/hub/venv/bin/postactivate

exec gunicorn -w $GUNICORN_WORKERS "queuinghub:create_app()"
```

22. Install supervisor and create configurations
```
sudo apt install supervisor
sudo touch /etc/supervisor/conf.d/hub.conf
```

23. Enter to edit the configurations
```
sudo nano /etc/supervisor/conf.d/hub.conf
```
and edit it to look like this:

```
[program:queuinghub]
command = /opt/hub/venv/scripts/start_gunicorn
autostart = true
autorestart = true
user = hub

stdout_logfile = /opt/hub/logs/gunicorn.log
redirect_stderr = true
```

24. Install supervisor
```
sudo -u hub mkdir /opt/hub/logs
```

25. Include your project in the Supervisor's configuration so the Supervisor can manage your program
```
sudo systemctl reload supervisor
```

26. You can check the status of your process
```
sudo supervisorctl
```
If this step is done successfully, it now runs on localhost.

27. To make the IP public, we are using nginx.
```
sudo apt install nginx
```

28. After installing the nginx, we are going to edit the configurations and "turn on" the site by enabling it.
```
sudo nano /etc/nginx/sites-available/hub
sudo ln -s /etc/nginx/sites-available/hub /etc/nginx/sites-enabled/hub
```
29. We also make sure to remove the default nginx configuration file.
```
sudo rm /etc/nginx/sites-enabled/default
```

30. The previously made changes are valid after you reload nginx. The new configuration become activate and should make the IP public on the internet after a reload if the network is set up correctly.
```
sudo systemctl reload nginx
```

31. Change file permissions to owner only and upload changes by reloading
```
sudo chmod 600 /opt/hub/venv/bin/postactivate
sudo systemctl reload nginx
```

32. You can check the nginx status or the supervisor status using the following commands 
```
sudo systemctl status nginx
sudo supervisorctl status
```

33. You should also now be able to test the HTTP endpoints using curls.

