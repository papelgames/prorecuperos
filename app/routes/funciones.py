from app.schemas.post import Users, Recuperos

class Asignador:
    def __init__ (self, puesto, equipo, estado):
        self.lista_users_activos = []
        #Users.query.all()
        self.ultimo_user_asignado = None
        self.puesto = puesto
        self.equipo = equipo
        self.estado = estado

    def listar_users_activos(self):
        for usuario in Users.query.filter_by(puesto = self.puesto, equipo = self.equipo, stestado = self.estado ).all():
            print(usuario)
            #self.lista_users_activos.append(usuario)
    
