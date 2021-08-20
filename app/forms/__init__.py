#-*- coding: utf-8 -*-
from wtforms import Form, StringField, TextField, PasswordField, IntegerField, SelectField, FileField, DateField, FloatField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required, Email, Length, NumberRange, Optional


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
        Length (min=6, max=15, message = 'El nombre de usuario debe tener de 6 a 10 caracteres')      
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
    
    nombre = StringField('Nombre', 
        validators=[Required('Debe completar el apellido')
        ])
    apellido = StringField('Apellido', 
        validators=[Required('Debe completar el apellido')
        ])
    phone = IntegerField('Número de teléfono',
        validators = [Optional()
        ])
    about = TextField('Sobre mi')
    
class PerfilesAmpliadosForm (PerfilesForm):    
    estado = SelectField('Estado', choices =[1], coerce = str, default = None)
    puesto = SelectField('Puesto', choices =[2], coerce = str, default = None)
    equipo = SelectField('Equipo', choices =[3], coerce = str, default = None)
    dependencia = SelectField('Dependencia', choices =['',4], coerce = str, default = None)


class PantallasForm (Form):
    formulario = SelectField('Nombre de la pantalla', choices =[], coerce = str, default = None,
        validators=[Required('Debe elegir una pantalla')
    ])

class UploadForm(Form):
    basexlsx = FileField('Excel')

class CobrosForm (Form):
    pagador =  StringField('Persona o compañía que paga',
        validators=[Required('Debe completar el nombre de la pantalla')        
    ])
    factura_nacion = StringField('Número factura de Nación Seguros',
    )
    cantidad_cuotas = SelectField('Cantidad de cuotas', choices =[1,2,3,4,5,6,7,8,9,10,11,12], coerce = str, default = None,
        validators=[Required('Debe elegir en cuantas cuotas se va a cobrar')
    ])
    importe_total = FloatField('Importe total del recupero')
    
class ImportesCobrosForm(Form):
    estado_cobro = SelectField('Nombre de la pantalla', choices =[], coerce = str, default = None,
        validators=[Required('Debe elegir una pantalla')
    ])
    fe_probable_cobro = DateField('Fecha Probable de cobro', format='%Y-%m-%d')
    fe_cobro =  DateField('Fecha de cobro', format='%Y-%m-%d')
    cuenta_bancaria =  StringField('Cuenta de nación')
    numero_cuota = IntegerField('Número de cuota')
    importe_cuota = FloatField('Importe de cuota')
    