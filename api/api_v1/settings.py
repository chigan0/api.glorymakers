import os
basedir = os.path.abspath(os.path.dirname(__file__))+'/models/'

class Config(object):
	DEBUG = True
	ENV = 'venv'
	CORS_HEADERS = 'Content-Type'
	SECRET_KEY = '975c3bb12c5b33353fe3436c0681cc568f21bbd8c86a7884b6b69497b564ce31'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'ted.db')
	SQLALCHEMY_BINDS = {
		'usersstat':'sqlite:///'+os.path.join(basedir,'users.db'),
	}
	MONGO_URI = 'mongodb://localhost:27017/test'
	LOGFILE = 'logs/v1.log'
	
	SQLALCHEMY_TRACK_MODIFICATIONS = False 
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = 'naz.abylai50@gmail.com'
	MAIL_PASSWORD = 'noyldtmuquyduzia'
	ERORS = {
		'UserAlreadyExistsError': {
			'message': "A user with that username already exists.",
			'status': 404,
		},
		'ResourceDoesNotExist': {
			'message': "A resource with that ID no longer exists.",
			'status': 500,
			'extra': "Any extra information you want.",
		},
	}

class DevelopmentConfig(Config):
	pass
	'''
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = 'naz.abylai50@gmail.com'
	MAIL_PASSWORD = 'noyldtmuquyduzia'
	'''

class TestingConfig(Config):
	pass