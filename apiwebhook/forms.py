from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from apiwebhook.models import Users

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(5,20)])
    remember = BooleanField('Lembrar Dados de Login')
    submit_login = SubmitField('Fazer Login')

class FormCadastro(FlaskForm):
    username = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(5,20)])
    confirm = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    token = StringField('Token', validators=[DataRequired()])
    submit_cadastro = SubmitField('Cadastrar')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('E-mail já cadastrado, Faça seu Login')

    def validate_token(self, token):
        if token.data != "uhdfaAADF123":
            raise ValidationError('Token Inválido')
