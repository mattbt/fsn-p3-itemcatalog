#from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, ColumnDefault, Boolean
from werkzeug import check_password_hash

from ..data import db #Base

class User(db.Model): #Base):
	__tablename__ = 'usertable'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80), nullable = False)
	email = db.Column(db.String(80), nullable = False)
	picture = db.Column(db.String(250))
	
	# if user registered in my app
	pwdhash = db.Column(db.String())
	activate = db.Column(db.Boolean)
	created = db.Column(db.DateTime)
		
	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)