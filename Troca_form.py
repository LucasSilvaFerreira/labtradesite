
from wtforms import Form, BooleanField, TextField, PasswordField, validators, StringField , IntegerField, FileField, TextAreaField
from wtforms.validators import DataRequired


class Registrar_nova_troca(Form):
    produto = StringField('produto', validators=[DataRequired()])
    quantidade = IntegerField('quantidade', validators=[DataRequired()])
    descricao = TextAreaField('descricao', validators=[DataRequired()])
    foto_produto = FileField('foto_produto')
