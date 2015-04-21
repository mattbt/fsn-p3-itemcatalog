import time

#from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, ColumnDefault
#from sqlalchemy.orm import relationship

from ..data import db #Base
from ..users.models import User

class Category(db.Model):
	__tablename__ = 'category'
	
	name = db.Column(db.String(80), nullable = False)
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('usertable.id'))
	usertable = db.relationship(User)
	insertDateTime = db.Column(db.DateTime, nullable = False)

	def get_dict(self, items):
		# returns object data in easily serializable format
		return {
			'name': self.name,
			'id': self.id,
                        'Items': [i.serialize for i in items]
		}

class Item(db.Model):
	__tablename__ = 'item'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80), nullable = False)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	category = db.relationship(Category)
	description = db.Column(db.String(250))
	user_id = db.Column(db.Integer, db.ForeignKey('usertable.id'))
	usertable = db.relationship(User)
	insertDateTime = db.Column(db.DateTime, default=time.time(), nullable = False)
	
	@property
	def serialize(self):
		# returns object data in easily serializable format
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description,
			'insertDateTime': self.insertDateTime
		}

		
