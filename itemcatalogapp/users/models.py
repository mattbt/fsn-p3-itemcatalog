#from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, ColumnDefault, Boolean
from werkzeug import check_password_hash
from flask.ext.login import UserMixin

from ..data import db #Base

class User(db.Model, UserMixin): #Base):
	__tablename__ = 'usertable'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80), nullable = False)
	email = db.Column(db.String(80), nullable = False)
	picture = db.Column(db.String(250))
	
	# if user registered in my app
	password = db.Column(db.String())
	activate = db.Column(db.Boolean)
	created = db.Column(db.DateTime)
		
	def check_password(self, password):
		return check_password_hash(self.password, password)
                #return (self.password == password)


'''
### Test Flask-User
	# Define User model. Make sure to add flask.ext.user UserMixin !!!
class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)

        # User Authentication information
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, default='')
        reset_password_token = db.Column(db.String(100), nullable=False, default='')

        # User Email information
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())

        # User information
        is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
        first_name = db.Column(db.String(50), nullable=False, default='')
        last_name = db.Column(db.String(50), nullable=False, default='')
        picture = db.Column(db.String(250))

        def is_active(self):
                return self.is_enabled

        def check_password(self, password):
                return check_password_hash(self.password, password)
        #return (self.password == password)
'''
'''### test Flask-Security
from flask.ext.security import UserMixin, RoleMixin

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String(255))
    picture = db.Column(db.String(250))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))'''
