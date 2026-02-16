# Meetings minutes

## Meeting 1.
* **DATE: 03.02.2026**
* **PARTICIPANTS: Leon Piikivi, Eira Paakkunainen, Teemu Puro, Amanda Korhonen**
* **TEACHER: Mika Oja**

### Action points
- In the wiki the examples of different clients should be separated
- Give an example of a client that isn't a human operator
- Some mistakes in the text: client vs. customer
- Think about resources in the future so that we have enough

### Notes 
Discussed the necessity of user table in database. It's not really needed in the API but in our plan it was just in the database if someone decides they want to use it. Concluded that since it's in the database but not in API it can be left as is. 

## Meeting 2.
* **DATE: 13.02.2026**
* **PARTICIPANTS: Leon Piikivi, Eira Paakkunainen, Teemu Puro, Amanda Korhonen**
* **TEACHER: Iván Sánchez Milara**

### Action points
- Currently, we have four clear resources. For the next deadline, we must think and implement one more resource to meet the requirements.
- README should recommend using requirements.txt and running db_populate.py afterwards. 
- README also needs polishing. For example, we had left the teacher's instructions visible.
- In database.py, in class Place, the line _queue = db.relationship("Queue", cascade="all, delete-orphan", back_populates = "place")_, the variable name should be queues instead of queue. This is due to the one-to-many relationship, as an establishment can have multiple queues. 

### Notes
*Add here notes that you consider important. This is not mandatory*


## Meeting 3.
* **DATE:**
* **PARTICIPANTS:**
* **TEACHER:**

### Action points
*List here the actions points discussed with assistants*

### Notes
*Add here notes that you consider important. This is not mandatory*


## Meeting 4.
* **DATE:**
* **PARTICIPANTS:**
* **TEACHER:**

### Action points
*List here the actions points discussed with assistants*

### Notes
*Add here notes that you consider important. This is not mandatory*


## Midterm meeting
* **DATE:**
* **PARTICIPANTS:**
* **TEACHER:**

### Action points
*List here the actions points discussed with assistants*

### Notes
*Add here notes that you consider important. This is not mandatory*


## Final meeting
* **DATE:**
* **PARTICIPANTS:**
* **TEACHER:**

### Minutes
*Summary of what was discussed during the meeting*

### Notes
*Add here notes that you consider important. This is not mandatory*



