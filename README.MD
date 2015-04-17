Item Catalog Project
===
##### Flask web app for handling an Item Catalog

How to test Item Catalog App

Using Vagrant
- download the project folder in a vagrant shared folder
- start and connect to vagrant VM
- install Python 2.7
- install postgresSQL
- install virtualenvwrapper module
 `pip install virtualenvwrapper`
- navigate to the project folder
- mkvirtualenv --python==path/to/python2.7 path/to/virtual/environments/folder/customprojectname
where path/to/virtual/environments/folder/ should be not in vagrant shared folders
- config postactivate file: nano path/to/virtual/environments/folder/customprojectname/bin/postactivate, add following lines:
 `cd path/to/project
export APP_SETTINGS="Config.DevelopmentConfig"
export DATABASE_URL="postgresql:///p3"`
- activate virtual environment
 `workon p3`
- create database - connect to psql with command `psql` and run 
 `create database p3`
- install required modules
 `pip install -r requirements.txt`
- run application
 `python run.py`
- open http://localhost:5000/catalog/ and try the app

![Alt text](/../screenshots/screenshots/itemcatalog1.png?raw=true "Optional Title")
---
>### ADDITIONAL NOTES
- facebook secrets file (/itemcatalogapp/users/fb_client_secrets.json) do not contain real app values. To test those functionalities consider creating your app and filling that file with "app_id" and "app_secret"
- google secrets file (/itemcatalogapp/users/client_secrets.json) do not contain real app values. To test those functionalities consider creating your app (https://console.developers.google.com) and then fill json file
