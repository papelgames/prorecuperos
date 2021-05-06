import os

UPLOAD_FOLDER = os.path.abspath(".\\uploads\\")
DB_URI = "vacio"



class Config(object):
    DEBUG = False
    SECRET_KEY = 'h\x1c\x9b\xbe\x16\n\xaaJ\xcaK?{\xc9e\xfdB\xa3'
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAIL_SERVER = os.environ["MAIL_SERVER"]
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ["MAIL_USERNAME"]
    MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
    DONT_REPLY_FROM_EMAIL = 'Prorecuperos'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

class ProductionConfig(Config):
    # SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = DB_URI
    

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(".\\database.db")
