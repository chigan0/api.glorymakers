from flask import Flask
from flask_restful import Api,Resource,reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS,cross_origin
from flask_socketio import SocketIO
from flask_pymongo import PyMongo
from settings import Config
from logging.handlers import RotatingFileHandler
from logging import Formatter
import logging

app = Flask(__name__)
app.config.from_object(Config)
handler = RotatingFileHandler(app.config['LOGFILE'],maxBytes=1000000,backupCount=1)
api= Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
cors = CORS(app, resources={r"/v1/*": {"origins": "*"}})
socketio = SocketIO(app,cors_allowed_origins="*")
mongo = PyMongo(app)

handler.setLevel(logging.DEBUG)
handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s ''[in %(pathname)s:%(lineno)d]'))
app.logger.addHandler(handler)

from models.models import *