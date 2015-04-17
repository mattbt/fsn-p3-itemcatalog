from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# build objects to handle db connection
Base = declarative_base()

#engine = create_engine('sqlite:///itemcatalogappwithusers.db')
engine = create_engine(os.environ['DATABASE_URL'])
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()