# Project Introduction 

This is an **Appointment System** for **Pet Grooming Service**.

**NOTE**: This system is still under development phase. 

Update Date:`13May 2018`


Subsystem|Status
:-- | --- 
User Register| Done 
User Login| Done 
Pet Add/Update/Delete| Done 
Card Add/Update/Delete| Done
Appointment Management| Done
Admin-Appointment Mgt| Done
Admin-Service Mgt| Done
Admin-Reminder Mgt| Done
Admin-Administrator Mgt| Done
Appointment Credit| Pending


## Requirements
This project is based on python 3.6.1

## How to start
##### config your db information 
Note: default is sqlite3 with the db file under project folder `$project_folder/app/app.db`

Or You can modify parameter `SQLALCHEMY_DATABASE_URI` in file  `app/config.py`.

##### open a python console at tha project folder
```shell
cd $project_folder
pip install -r requirement.txt
# open a python3 console
python
```
##### create tables and mock data
```python
import mockdata as mk
mk.mock()
```

##### start this system
```shell
cd $project_folder
python run.py
```
Now you can see this system using [http://127.0.0.1:5001](http://127.0.0.1:5001) by default.