#-*- coding: utf-8 -*-
from wtforms import Form, StringField, TextField, validators, PasswordField, IntegerField
from wtforms.fields.html5 import EmailField

class LoginForm(Form):
    username = StringField('Usuario', [
        validators.Required(message='El usuario no puede estar vacío.'),
        validators.length(min=1,max=11,message='El usuario no es válido')        
    ])
    password = PasswordField('Contraseña',[
        validators.Required(message='La contraseña no puede estar vacía'),
        validators.length(min=1,max=10,message='El usuario no es válido')
    ])