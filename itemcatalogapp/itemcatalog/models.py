import time

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, ColumnDefault
from sqlalchemy.orm import relationship

from ..data import Base
from ..users.models import User

class Category(Base):
	__tablename__ = 'category'
	
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, ForeignKey('usertable.id'))
	usertable = relationship(User)
	insertDateTime = Column(DateTime, nullable = False)

	def get_dict(self, items):
		# returns object data in easily serializable format
		return {
			'name': self.name,
			'id': self.id,
                        'Items': [i.serialize for i in items]
		}

class Item(Base):
	__tablename__ = 'item'

	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)
	description = Column(String(250))
	user_id = Column(Integer, ForeignKey('usertable.id'))
	usertable = relationship(User)
	insertDateTime = Column(DateTime, default=time.time(), nullable = False)
	
	@property
	def serialize(self):
		# returns object data in easily serializable format
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description,
			'insertDateTime': self.insertDateTime
		}

		
