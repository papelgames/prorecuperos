from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_mail import Mail
# import config 

import os
# import urllib.parse, hashlib

# from config import *

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch = True)
mail = Mail (app)
from app.routes import *