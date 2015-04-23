import os

# available languages
LANGUAGES = {
	'en': 'English',
	'it': 'Italian'
}

class Config(object):
	DEBUG = False
	TESTING = False
	CSRF_EANBLED = True
	SECRET_KEY = 'wefergasdtehgbsrtrge546'
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	BABEL_DEFAULT_LOCALE = 'en'
	BABEL_DEFAULT_TIMEZONE = 'UTC'
	LANGUAGE = 'it'
	
	SECURITY_REGISTERABLE = True
	SECURITY_CONFIRMABLE = False
	SECURITY_CHANGEABLE = True
	SECURITY_SEND_REGISTER_EMAIL = False

	
class ProductionConfig(Config):
	DEBUG = False
	
class StagingConfig(Config):
	DEVELOPMENT = True
	DEBUG = True

class DevelopmentConfig(Config):
	DEVELOPMENT = True
	DEBUG = True
	
class TestingConfig(Config):
	TESTING = True