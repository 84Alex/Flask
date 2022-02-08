from email_validator import validate_email
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, length


class Login (FlaskForm):
    user = StringField('Usuario', validators=[
        DataRequired('El Campo Usuario es Obligatorio'),
        Email(message='El correo ingresado no es valido'),
        length(min=3, max=255)
    ])
    passw = PasswordField('Contraseña', validators=[
        DataRequired('El Campo Password es Obligatorio'),
        length(min=8, max=12, message='La contraseña debe contener minimo 8 caracteres y maximo 12')
    ])
    submit = SubmitField('submit')