from apiwebhook import database, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)

class Dados(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False)
    status = database.Column(database.String, nullable=False)
    valor = database.Column(database.String, nullable=False)
    forma_pagamento = database.Column(database.String, nullable=False)
    parcelas = database.Column(database.Integer, nullable=False)
    msg_liberar_acesso = database.Column(database.Boolean, nullable=False, default=False)
    msg_retirar_acesso = database.Column(database.Boolean, nullable=False, default=False)
    msg_boas_vindas = database.Column(database.Boolean, nullable=False, default=False)
    msg_recusado = database.Column(database.Boolean, nullable=False, default=False)
    data = database.Column(database.DateTime, default=datetime.utcnow)
