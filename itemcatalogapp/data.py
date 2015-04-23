# SQL-Alchemy
from . import app
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
dbsession = db.session

# Setup Flask-Security
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required, current_user, login_user, logout_user
from .users.models import User, Role
from .users.forms import ExtendedRegisterForm
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)


