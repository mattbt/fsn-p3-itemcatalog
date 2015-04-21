import os

# initialize app
from flask import Flask
app = Flask(__name__)

# load config
app.config.from_object(os.environ['APP_SETTINGS'])

# import translations and international settings
from .translations import babel

# import and register Blueprints
from .itemcatalog.views import itemcatalogbp
from .users.views import usersbp

app.register_blueprint(itemcatalogbp)
app.register_blueprint(usersbp)

### import db object and create tables if they don't exist
from .data import db
db.create_all()

