#-*- coding: utf-8 -*-
from wtforms import Form, StringField, TextField, PasswordField, IntegerField, SelectField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required, Email, Length


class LoginForm(Form):
    username = StringField('Usuario', 
        validators= [Required('El usuario no puede estar vacío.')
              
    ])
    password = PasswordField('Contraseña',
        validators= [Required('La contraseña no puede estar vacía.')
    ])

class SingupForm(Form):
    username = StringField('Usuario', 
        validators= [Required('El usuario no puede estar vacío.'),
        Length (min=6, max=10, message = 'El nombre de usuario debe tener de 6 a 10 caracteres')      
    ])
    email = EmailField('Correo Electronico',
        validators= [Required('El correo electrónico no puede estar vacío.'),
        Email(message ='No es el formato correcto para un correo electrónico')
    ])
    password = PasswordField('Contraseña',
        validators= [Required('La contraseña no puede estar vacía.'),
        Length (min=6, max=10, message = 'La contraseña debe tener de 6 a 10 caracteres.')
    ])    

class AbmTareasForm(Form):
    descripcion = StringField('Descripcion de la tarea',
        validators=[Required('Debe completar la descripcion de la tarea')        
    ])
    vencimiento= IntegerField('Dias para el vencimiento',
        validators=[Required('Los dias para el vencimiento no pueden estar vacíos')
    ])

class AbmPermisosForm (Form):
    formulario = StringField('Nombre de la pantalla',
        validators=[Required('Debe completar el nombre de la pantalla')        
    ])

class PerfilesForm (Form):
    username = SelectField('Nombre de usuario', choices =[], coerce = str, default = None,
        validators=[Required('Debe elegir un usuario')
    ])

class PantallasForm (Form):
    formulario = SelectField('Nombre de la pantalla', choices =[], coerce = str, default = None,
        validators=[Required('Debe elegir una pantalla')
    ])

class UploadForm(Form):
    basexlsx = FileField('Excel')
