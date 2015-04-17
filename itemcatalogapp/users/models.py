from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, ColumnDefault, Boolean
from werkzeug import check_password_hash

from ..data import Base

class User(Base):
	__tablename__ = 'usertable'
	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	email = Column(String(80), nullable = False)
	picture = Column(String(250))
	
	# if user registered in my app
	pwdhash = Column(String())
	activate = Column(Boolean)
	created = Column(DateTime)
		
	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)