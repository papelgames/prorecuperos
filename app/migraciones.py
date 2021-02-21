from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()  # Se crea un objeto de tipo Migrate

def create_app(settings_module):
    # Inicialización de los parámetros de configuración
    ...

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # db.init_app(app)
    # migrate.init_app(app, db)  # Se inicializa el objeto migrate

   