from app import db

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),\
                     onupdate=db.func.current_timestamp())

class Users(Base):
    __tablename__ = "users"
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
    recuperos = db.relationship("Recuperos")
    permisos_usuarios = db.relationship("Permisos", secondary = "usuariospermisos", backref="pu", lazy="dynamic")

class Recuperos (Base):
    __tablename__ = "recuperos"
    rama = db.Column(db.Integer)
    siniestro = db.Column(db.Integer)
    fe_ocurrencia = db.Column(db.DateTime)
    fe_denuncia = db.Column(db.DateTime)
    fe_pago = db.Column(db.DateTime)
    importe_pagado = db.Column(db.Float())
    compania = db.Column(db.String(50))
    estado = db.Column(db.Integer(), nullable=False)
    desc_sinestro = db.Column(db.Text())
    tercero = db.Column(db.String(50))
    tel_tercero = db.Column(db.String(50))
    mail_tercero = db.Column(db.String(50))
    asegurado = db.Column(db.String(50))
    monto_franquicia = db.Column(db.Float)
    responsabilidad = db.Column(db.Integer())
    usuario_responsable = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    tareas_pendientes = db.relationship ("TareasPendientes")
    

class Image(Base):
    __tablename__ = "image"
    filename = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    owner_username = db.Column(db.String(50), nullable=False)

class Acciones (Base):
    __tablename__ = "acciones"
    descripcion = db.Column(db.String(50), nullable=False)
    estado_recupero = db.Column(db.Integer)
    id_tarea_siguiente = db.Column(db.Integer, db.ForeignKey("tareas.id"))
    tareas = db.relationship("Tareas", secondary = "tareasacciones")

class Tareas (Base):
    __tablename__ = "tareas"
    descripcion = db.Column(db.String(50), nullable=False)
    vencimiento = db.Column(db.Integer, nullable=False)
    acciones = db.relationship("Acciones", secondary="tareasacciones")
    tareas_pendientes = db.relationship ("TareasPendientes")

class TareasAcciones (Base):
    __tablename__ = "tareasacciones"
    id_tarea = db.Column(db.Integer, db.ForeignKey("tareas.id"), primary_key = True)
    id_accion = db.Column(db.Integer, db.ForeignKey("acciones.id"), primary_key = True)

class TareasPendientes (Base):
    __tablename__ = "tareaspendientes"
    id_tarea = db.Column(db.Integer, db.ForeignKey("tareas.id"), nullable=False)
    id_recupero = db.Column(db.Integer, db.ForeignKey("recuperos.id"), nullable=False)
    fe_vencimiento = db.Column(db.DateTime, nullable = False)

class Permisos (Base):
    __tablename__ = "permisos"
    formulario = db.Column(db.String)
    #permisos_usuarios = db.relationship("Users", secondary = "usuariospermisos",backref="up", lazy="dynamic")

class UsuariosPermisos (Base):
    __tablename__ = "usuariospermisos"
    id_usuario = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key = True, nullable = False)
    id_permiso = db.Column(db.Integer, db.ForeignKey("permisos.id"), primary_key = True, nullable = False)