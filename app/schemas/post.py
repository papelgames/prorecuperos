from app import db

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),\
                     onupdate=db.func.current_timestamp())

class Users(Base):
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    nombre =db.Column(db.String(50), unique=False, nullable=True)
    apellido =db.Column(db.String(50), unique=False, nullable=True)
    password = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(22),nullable=True)
    about_me = db.Column(db.String(280), default="")
    status = db.Column(db.String(2), nullable=False)
    fe_ultima_contrasenia = db.Column(db.DateTime)
    images = db.relationship("Image", backref="owner", lazy="dynamic")

class Recuperos (Base):
    rama = db.Column(db.Integer)
    siniestro = db.Column(db.Integer)
    fe_ocurrencia = db.Column(db.DateTime)
    fe_denuncia = db.Column(db.DateTime)
    fe_pago = db.Column(db.DateTime)
    importe_pagado = db.Column(db.Float())
    compania = db.Column(db.String(50))
    estado = db.Column(db.String(2), nullable=False)
    desc_sinestro = db.Column(db.String(400))
    tercero = db.Column(db.String(50))
    tel_tercero = db.Column(db.String(50))
    mail_tercero = db.Column(db.String(50))
    asegurado = db.Column(db.String(50))
    monto_franquicia = db.Column(db.Float)
    responsabilidad = db.Column(db.String(2), nullable=True)
    usuario_responsable = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

class Image(Base):
    filename = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    owner_username = db.Column(db.String(50), nullable=False)