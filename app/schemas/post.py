from app import db

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),\
                     onupdate=db.func.current_timestamp())

class Users(Base):
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(22),nullable=True)
    about_me = db.Column(db.String(280), default="")
    images = db.relationship("Image", backref="owner", lazy="dynamic")

class Image(Base):
    filename = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    owner_username = db.Column(db.String(50), nullable=False)