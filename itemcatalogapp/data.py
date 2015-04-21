# SQL-Alchemy
from . import app
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
dbsession = db.session