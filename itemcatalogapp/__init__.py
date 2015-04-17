import os

# initialize app
from flask import Flask
app = Flask(__name__)

# load config
app.config.from_object(os.environ['APP_SETTINGS'])

# register and import Blueprints
from .itemcatalog.views import itemcatalogbp
from .users.views import usersbp

app.register_blueprint(itemcatalogbp)
app.register_blueprint(usersbp)

### import Base, engine and create DB if it doesn't exist
from sqlalchemy import create_engine
from .data import Base, engine
import itemcatalog.models

Base.metadata.create_all(engine) # adds classes as new tables in db

