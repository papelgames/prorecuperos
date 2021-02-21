from flask import Flask
from flask_sqlalchemy import SQLAlchemy


import config 

import os
import urllib.parse, hashlib

# from config import *

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

db = SQLAlchemy(app)

from app.routes import *