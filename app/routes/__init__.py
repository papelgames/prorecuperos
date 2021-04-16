from app import app, db
from flask import render_template, request, session, escape,\
                    redirect, url_for, flash, g, send_from_directory, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app.schemas.post import Users, Image, Tareas, Permisos, UsuariosPermisos, Recuperos
from app.forms import LoginForm, SingupForm, AbmTareasForm, AbmPermisosForm, PerfilesForm, PantallasForm, UploadForm

import urllib.parse, hashlib
import os
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpge", "gif", "pdf"])

def allowed_file(filename):

    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_profile_picture(email):
    default = "https://lh5.googleusercontent.com/fhcUNRdmwXqNpwf4kMHMPbn3y6eOOQnx4UfI3l0OfA308R-tI3e0cg3pFeEhxshDKyXRuZj9s8aHBqrFrmbR=w1366-h635"
    size = 512

    gravatar_url = "https://www.gravatar.com/avatar/" + \
                        hashlib.md5(email.encode("utf-8").lower()).hexdigest() + "?"
    gravatar_url += urllib.parse.urlencode({"d":default, "s":str(size)})

    return gravatar_url



'''         
prueba = db.session.query(Reclamo, Servicio, Cliente, Estado).\
         join(Reclamo.servicio, Reclamo.cliente, Reclamo.estado).\
         all()


'''
@app.before_request
def before_request():
    
    if "username" in session:
        g.user = session["username"]
        permisos_usuarios = Permisos.query.filter(Permisos.pu.any(username = g.user)).all()
        #g.id_permisos = []
        #for per in permisos_usuarios:
        #    g.id_permisos.append(per.formulario) 
        
    else:
        g.user = None
   
@app.route("/")
def index():
   
    return render_template("index.html")




@app.route("/search")
def search():
    username = request.args.get("username")

    return redirect(url_for("profile", username=username))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    singup_form = SingupForm(request.form)
    if not g.user:
        if request.method == "POST" and singup_form.validate():
            
            username = Users.query.filter_by(username=singup_form.username.data.lower()).first()
            email = Users.query.filter_by(email=singup_form.email.data.lower()).first()
            
            if username:
                flash("El usuario ya existe", "alert-warning")
                return redirect(request.url)
          
            if email:
                flash("El correo electronico ya existe", "alert-warning")
                return redirect(request.url)

            hashed_pw = generate_password_hash(singup_form.password.data, method="sha256")
            new_user = Users(username=singup_form.username.data.lower(), 
                            email=singup_form.email.data.lower(), password=hashed_pw,
                                status=1, 
                                puesto = 1, 
                                equipo = 1)
            db.session.add(new_user)
            db.session.commit()

            flash("Se registro correctamente.", "alert-success")

            return redirect(url_for("login"))

        return render_template("signup.html", form = singup_form)
    flash("Ya tienes una cuenta para loguearte.", "alert-primary")

    return redirect(url_for("home"))

@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm(request.form)
    if not g.user:
        if request.method == "POST" and login_form.validate():
            username = login_form.username.data 
            password = login_form.password.data
            
            user = Users.query.filter_by(username=username\
                        .lower()).first()
            

            if user and check_password_hash(user.password, password):
                session["username"] = user.username
                flash("Ahora te encuentras logueado.", "alert-success")
                return redirect("home")
            flash("Tus credenciales no son válidas. Vuelve a intentarlo.", "alert-warning")

        return render_template("login.html", form = login_form)
    flash("Ya te encuentras logueado", "alert-primary")

    return redirect(url_for("home")) 


@app.route("/profile/<username>")
def profile(username):
    user = Users.query.filter_by(username=username).first()

    if user:
        files = user.images.order_by(Image.date_modified).limit(10).all()
        picture = get_profile_picture(user.email)
        
        return render_template("profile.html", user=user, files=files, picture=picture)
    
    abort(404)

@app.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    user = Users.query.filter_by(username=g.user).first()

    if request.method == "POST":
        user.about_me = request.form["about"]
        user.phone = request.form["phone"]
        db.session.commit()

        flash("Changes has been saved successfully!", "alert-success")
        return redirect(url_for("profile", username=g.user))

    return render_template("edit_profile.html", user=user)

@app.route("/home", methods=["GET", "POST"])
def home():
    if g.user:
        if request.method == "POST":
            if "file" not in request.files:
                flash("No file part.", "alert-danger")
                return redirect(request.url)
            file = request.files["file"]
            if file.filename == "":
                flash("No selected file.", "alert-warning")
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                user = Users.query.filter_by(username=g.user).first()
                file_to_db = Image(filename=filename, owner=user, \
                                owner_username=user.username)
                print(file)
                db.session.add(file_to_db)
                db.session.commit()
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                return redirect(url_for("get_files"))
        return render_template("home.html")
    flash("You must be logged in.", "alert-warning")

    return redirect(url_for("login"))

@app.route("/basexlsx", methods=["GET", "POST"])
def basexlsx():
    basexlsx_form = UploadForm(request.form)
    if g.user:
        if request.method == "POST" and basexlsx_form.validate():
            # image_data = request.FILES[form.image.name].read()
            if basexlsx_form.basexlsx.name not in request.files:
                flash("No se ha seleccionado ningun archivo", "alert-danger")
                return redirect(request.url)
            file = request.files[basexlsx_form.basexlsx.name]
            print (file)
            if file.filename == "":
                flash("No selected file.", "alert-warning")
                return redirect(request.url)
            if file:# and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                import openpyxl 
                documento = openpyxl.load_workbook(os.path.abspath(app.config["UPLOAD_FOLDER"] + '\\' + filename))
                
                ws = documento.active
                smq = (ws.rows)
                
                registros_nuevos = 0
                registros_repetidos = 0
                registros_total = 0
                for campo in smq:
                    registros_total +=1
                    if Recuperos.query.filter_by (rama = campo[0].value).first() and \
                       Recuperos.query.filter_by (siniestro = campo[1].value).first():
                       registros_repetidos += 1
                       continue
                    rama = campo[0].value 
                    siniestro = campo[1].value
                    desc_siniestro = campo[2].value
                    fe_ocurrencia = campo[3].value
                    importe_pagado = campo[4].value
                    estado = 1
                    
                    registro_recupero = Recuperos(rama = rama,\
                                                  siniestro = siniestro,\
                                                  desc_siniestro = desc_siniestro,\
                                                  fe_ocurrencia = fe_ocurrencia,\
                                                  importe_pagado =importe_pagado,\
                                                  estado = estado)
                    db.session.add(registro_recupero)
                    registros_nuevos += 1
                db.session.commit()
                flash("Se han ingresado: " + str(registros_nuevos) + " nuevos registros. Se rechazaron: " + \
                    str(registros_repetidos) + " registros ya existentes. El archivo contenia: " + str(registros_total) \
                        + " registros.", "alert-primary" )

        return render_template("subirbases.html", form = basexlsx_form)
    flash("You must be logged in.", "alert-warning")

    return redirect(url_for("login"))


@app.route("/files")
def get_all_files():
    files = Image.query.order_by(Image.date_modified).limit(200).all()

    return render_template("files.html", files=files)

@app.route("/perfiles/", methods=["GET", "POST"])
@app.route("/perfiles/<username>", methods=["GET", "POST"])
def perfiles(username = "vacio"):
    #falta validar el form  y si está el usuario logueado
    perfil_usuario_Form = PerfilesForm(request.form)
    perfil_usuario = Permisos.query.filter(Permisos.pu.any(username = username)).all()
    pantalla_Form = PantallasForm(request.form)
    
    perfil_usuario_Form.username.choices = [""]
    
    for i in Users.query.all():
        perfil_usuario_Form.username.choices.append (i.username)

        

    pantalla_Form.formulario.choices = [""]

    for i  in Permisos.query.all():
        pantalla_Form.formulario.choices.append (i.formulario )
    
    
    
    if request.method == "POST" and pantalla_Form.validate():
        
        id_usuario = Users.query.filter_by (username = username).first().id
        id_permiso = Permisos.query.filter_by(formulario = pantalla_Form.formulario.data).first().id

        nuevo_permiso_en_usuario = UsuariosPermisos(id_usuario=id_usuario, \
                                                    id_permiso = id_permiso)

        db.session.add(nuevo_permiso_en_usuario)
        db.session.commit()

        flash("Se a generado una nueva permiso", "alert-success")
        url_for("perfiles", username=username)
        #redirect(url_for("perfiles", username = perfil_usuario_Form.username.data))  
    return render_template("perfiles.html", form = perfil_usuario_Form, \
                                            perfil_usuario = perfil_usuario, \
                                            form2 = pantalla_Form)
    

@app.route("/buscarperfil")
def buscarperfil():
    username = request.args.get("username")

    return redirect(url_for("perfiles", username=username))

@app.route("/myfiles")
def get_files():
    if g.user:
        user = Users.query.filter_by(username=g.user).first()

        if user.images.all():
            files = user.images.order_by(Image.date_modified).all()
            return render_template("my_files.html", files=files)
        
        files = []
        return render_template("my_files.html", files=files)

    flash("You must be logged in.", "alert-warning")

    return redirect(url_for("login"))

@app.route('/uploads/<filename>')
def uploaded_file(filename):

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You're logged out.", "alert-secondary")

    return redirect(url_for("index"))

@app.route("/abmtareas", methods=["GET", "POST"])
def abmtareas():
    abmtareas_form = AbmTareasForm(request.form)
    if g.user:
        if request.method == "POST" and abmtareas_form.validate():
            
            descripcion = abmtareas_form.descripcion.data
            vencimiento = abmtareas_form.vencimiento.data

            nuevo_reg_tarea = Tareas(descripcion=descripcion, vencimiento=vencimiento)

            db.session.add(nuevo_reg_tarea)
            db.session.commit()

            flash("Se a generado una nueva tarea", "alert-success")

            return redirect(url_for("abmtareas"))       
            
        return render_template("abmtareas.html", form = abmtareas_form)
    flash("Primero debes loguearte", "alert-warning")
    return redirect(url_for("login"))

@app.route("/abmpermisos", methods=["GET", "POST"])
def abmpermisos():
    abmpermisos_form = AbmPermisosForm(request.form)
    if g.user:
        if request.method == "POST" and abmpermisos_form.validate():
            
            formulario = abmpermisos_form.formulario.data
            
            nuevo_reg_permiso = Permisos(formulario=formulario)

            db.session.add(nuevo_reg_permiso)
            db.session.commit()

            flash("Se a generado una nueva permiso", "alert-success")

            return redirect(url_for("abmpermisos"))       
            
        return render_template("abmpermisos.html", form = abmpermisos_form)
    flash("Primero debes loguearte", "alert-warning")
    return redirect(url_for("login"))


@app.route("/about")
def about():

    return render_template("about.html")
    
@app.errorhandler(404)
def page_not_found(error):

    return render_template("404_page_not_found.html"), 404

