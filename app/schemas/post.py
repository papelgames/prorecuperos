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
    status = db.Column(db.Integer, nullable=False) #tabla estados <parametro tabla users>
    fe_ultima_contrasenia = db.Column(db.DateTime)
    puesto = db.Column(db.Integer, nullable = False) #tabla puestosusuarios
    equipo = db.Column(db.Integer, nullable = False) #tabla equiposusuarios
    dependencia = db.Column(db.Integer) #debe ir el id de otro user
    images = db.relationship("Image", backref="owner", lazy="dynamic")
    recuperos = db.relationship("Recuperos")
    puestos_usuarios = db.relationship("PuestosUsuarios")
    equipos_usuarios = db.relationship("EquiposUsuarios")
    permisos_usuarios = db.relationship("Permisos", secondary = "usuariospermisos", backref="pu", lazy="dynamic")
    
class PuestosUsuarios (Base):
    __tablename__ ="perfilesusuarios"
    puesto = db.Column(db.String(20), unique=True, nullable=False)
    sub_codigo = db.Column(db.String(2), unique=True)
    id_username = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

class EquiposUsuarios (Base):
    __tablename__ = "equiposusuarios"
    equipo = db.Column(db.String(20), unique=True, nullable=False)
    sub_codigo = db.Column(db.String(2), unique=True)
    id_username = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

class Recuperos (Base):
    __tablename__ = "recuperos"
    rama = db.Column(db.Integer)
    siniestro = db.Column(db.Integer)
    fe_ocurrencia = db.Column(db.DateTime)
    fe_denuncia = db.Column(db.DateTime)
    fe_pago = db.Column(db.DateTime)
    importe_pagado = db.Column(db.Float())
    compania = db.Column(db.Integer) #tabla companias
    comprador = db.Column(db.Integer) #tabla comprador
    estado = db.Column(db.Integer()) #tabla estados <parametro tabla recuperos>
    desc_siniestro = db.Column(db.Text())
    tercero = db.Column(db.String(50))
    tel_tercero = db.Column(db.String(50))
    mail_tercero = db.Column(db.String(50))
    asegurado = db.Column(db.String(50))
    poliza = db.Column(db.Integer)
    monto_franquicia = db.Column(db.Float)
    responsabilidad = db.Column(db.Integer()) #tabla respondabilidades
    analista_siniestro = db.Column(db.String(4)) #alfanumerico de GLM 
    usuario_responsable = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    tareas_pendientes = db.relationship ("TareasPendientes")
    cobros = db.relationship ("Cobros")
    

class Responsabilidades (Base):
    desc_responsabilidad = db.Column(db.String(50), nullable = False)

class Companias (Base):
    __tablename__ = "companias"
    nombre = db.Column(db.String(50), nullable= False)
    telefono = db.Column(db.String(50))
    correos = db.Column(db.Integer) 
    correos_electronicos = db.relationship ("CorreosElectronicos")

class Compradores (Base):
    __tablename__ = "compradores"
    nombre = db.Column(db.String(50), nullable= False)
    telefono = db.Column(db.String(50))
    correos = db.Column(db.Integer) 
    correos_electronicos = db.relationship ("CorreosElectronicos")

class CorreosElectronicos (Base):
    __tablename__ = "correoselectronicos"
    correo = db.Column(db.String(50), nullable = False)
    id_compania = db.Column(db.Integer, db.ForeignKey("companias.id"), nullable = False)
    id_comprador = db.Column(db.Integer, db.ForeignKey("compradores.id"), nullable = False)

class Image(Base):
    __tablename__ = "image"
    filename = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    owner_username = db.Column(db.String(50), nullable=False)

class Acciones (Base):
    __tablename__ = "acciones"
    descripcion = db.Column(db.String(50), nullable=False)
    estado_recupero = db.Column(db.Integer)
    envia_correo = db.Column(db.String(2))
    destinatario_correo = db.Column(db.String(2))
    id_tarea_siguiente = db.Column(db.Integer, db.ForeignKey("tareas.id"))
    tareas = db.relationship("Tareas", secondary = "tareasacciones", backref = "ta", lazy="dynamic")

class Tareas (Base):
    __tablename__ = "tareas"
    descripcion = db.Column(db.String(50), nullable=False)
    vencimiento = db.Column(db.Integer, nullable=False)
    acciones = db.relationship("Acciones", secondary="tareasacciones", backref="ta", lazy= "dynamic")
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
    formulario = db.Column(db.String(20))
    permisos_usuarios = db.relationship("Users", secondary = "usuariospermisos",backref="up", lazy="dynamic")

class UsuariosPermisos (Base):
    __tablename__ = "usuariospermisos"
    usuario_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    permiso_id = db.Column(db.Integer, db.ForeignKey("permisos.id"), nullable = False)

class Estados (Base):
    __tablename__ = "estados"
    desc_estado = db.Column(db.String(15), nullable = False)
    estado_tabla = db.Column(db.String(30), nullable = False)
    sub_codigo = db.Column(db.String(2), unique=True)

class Cobros (Base):
    __tablename__ = "cobros"
    pagador = db.Column(db.String(50), nullable = False)
    factura_nacion = db.Column(db.String(13))
    cantidad_cuotas = db.Column(db.Integer)
    importe_total = db.Column(db.Float)
    id_recupero = db.Column(db.Integer, db.ForeignKey("recuperos.id"), nullable=False)
    importes_cobros = db.relationship("ImportesCobros")

class ImportesCobros (Base):
    __tablename__ = "importescobros"    
    estado_cobro = db.Column(db.Integer)
    fe_probable_cobro = db.Column(db.DateTime)
    fe_cobro = db.Column(db.DateTime)
    cuenta_bancaria = db.Column(db.String(50))
    numero_cuota = db.Column(db.Integer)
    importe_cuota = db.Column(db.Float)
    id_cobro = db.Column(db.Integer, db.ForeignKey("cobros.id"),  nullable = False)
    
class Observaciones (Base):
    __tablename__ = "observaciones"
    observacion = db.Column(db.Text)
    id_recupero = db.Column(db.Integer)
    id_cobro = db.Column(db.Integer)
    id_tarea_pendiente = db.Column(db.Integer)
    id_user = db.Column(db.Integer, nullable = False)