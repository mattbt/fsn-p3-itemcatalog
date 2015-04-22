# SQL-Alchemy
from . import app
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
dbsession = db.session

'''# Setup Flask-Security
from .users.models import User, Role
from flask.ext.security import Security, SQLAlchemyUserDatastore
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)'''

# Setup Flask-login
from flask.ext.login import LoginManager
from .users.models import User
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    '''Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    '''
    return User.query.get(id)