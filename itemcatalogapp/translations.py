from . import app
from flask.ext.babel import Babel
from flask import g, request
from config import LANGUAGES
babel = Babel(app)

# get language
@babel.localeselector
def get_locale():
    # if language forced
    if 'LANGUAGE'in app.config:
        if app.config['LANGUAGE'] in LANGUAGES.keys():
	    return app.config['LANGUAGE']
	else:
            print 'Language not found in Config - LANGUAGES'
    # else if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    
    if user is not None:
	print user.locale
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.
    return request.accept_languages.best_match(LANGUAGES.keys()) # 'it'

# get international timezone
@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone
