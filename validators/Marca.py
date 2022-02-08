import required as required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, length


class Marca(FlaskForm):
    marca = StringField('Marca', validators=[
        DataRequired('El campo marca es Obligatorio'),
        length(min=3, max=255)
    ])
    description = TextAreaField('Descripcion', validators=[
        DataRequired('El campo descripcion es Obligatorio'),
        length(min=3, max=1000)
    ])
    # create_at = DateField('Fecha de Creacion', validators=[
        # DataRequired('Debe seleccionar una Fecha de Creacion')
    # ])


