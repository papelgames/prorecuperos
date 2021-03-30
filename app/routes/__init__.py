from app import app, db
from flask import render_template, request, session, escape,\
                    redirect, url_for, flash, g, send_from_directory, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app.schemas.post import Users, Image, Tareas
from app.forms import LoginForm, SingupForm, AbmTareasForm

import urllib.parse, hashlib

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


@app.before_request
def before_request():
    if "username" in session:
        g.user = session["username"]
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
            new_user = Users(username=singup_form.username.data.lower(), \
                            email=singup_form.email.data.lower(), password=hashed_pw,\
                                status="a")
            db.session.add(new_user)
            db.session.commit()

            flash("Se registro correctamente.", "alert-success")

            return redirect(url_for("login"))

        return render_template("signup.html", form = singup_form)
    flash("You're already logged in.", "alert-primary")

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
                flash("Now you're logged in.", "alert-success")
                return redirect("home")
            flash("Your credentials are invalid, check and try again.", "alert-warning")

        return render_template("login.html", form = login_form)
    flash("You are already logged in.", "alert-primary")

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
                db.session.add(file_to_db)
                db.session.commit()
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                return redirect(url_for("get_files"))
        return render_template("home.html")
    flash("You must be logged in.", "alert-warning")

    return redirect(url_for("login"))

@app.route("/files")
def get_all_files():
    files = Image.query.order_by(Image.date_modified).limit(200).all()

    return render_template("files.html", files=files)


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

@app.route("/about")
def about():

    return render_template("about.html")
    
@app.errorhandler(404)
def page_not_found(error):

    return render_template("404_page_not_found.html"), 404



