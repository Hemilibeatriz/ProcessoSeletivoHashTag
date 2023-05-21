from flask import render_template, redirect, url_for, flash, request
from apiwebhook import app, database, bcrypt
from apiwebhook.forms import FormLogin, FormCadastro
from apiwebhook.models import Users, Dados
from flask_login import login_user, logout_user, current_user, login_required
import requests
import json
from datetime import datetime

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    form_cadastro = FormCadastro()
    if form_cadastro.validate_on_submit():
        password_crypt = bcrypt.generate_password_hash(form_cadastro.password.data)
        user = Users(username=form_cadastro.username.data, email=form_cadastro.email.data, password=password_crypt)
        database.session.add(user)
        database.session.commit()
        flash(f'Cadastro Feito Com Sucesso Para o Usuário {form_cadastro.username.data}', 'alert-success')
        return redirect(url_for('login'))
    return render_template("cadastro.html", form_cadastro = form_cadastro)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        user = Users.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user, remember=form_login.remember.data)
            flash(f'Login Feito Com Sucesso Para o E-mail {form_login.email.data}', 'alert-success')
            next = request.args.get('next')
            if next:
                return redirect(next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha no Login. E-mail ou Senha Incorretos', 'alert-danger')
    return render_template("login.html", form_login = form_login)

@app.route("/sair")
@login_required
def sair():
    logout_user()
    flash('Logout Feito Com Sucesso', 'alert-success')
    return redirect(url_for('home'))

@app.route("/webhook", methods=['POST'])
def webhook():
    conteudo_bruto = request.data
    if conteudo_bruto:
        conteudo_string = conteudo_bruto.decode("utf-8")
        conteudo_json = json.loads(conteudo_string)
        dado = Dados(
            nome=conteudo_json.get("nome"),
            email=conteudo_json.get("email"),
            status=conteudo_json.get("status"),
            valor=conteudo_json.get("valor"),
            forma_pagamento=conteudo_json.get("forma_pagamento"),
            parcelas=conteudo_json.get("parcelas"),
            msg_liberar_acesso=True if conteudo_json.get("status") == "aprovado" else False,
            msg_boas_vindas=True if conteudo_json.get("status") == "aprovado" else False,
            msg_recusado=True if conteudo_json.get("status") == "recusado" else False,
            msg_retirar_acesso=True if conteudo_json.get("status") == "reembolsado" else False,
            data=datetime.utcnow())
        if conteudo_json.get("status") == "aprovado":
            print(f"Enviar Mensagem de Boas Vindas Para o Usuário {conteudo_json.get('email')}")
            print(f"Enviar Mensagem de Acesso Liberado Para o Usuário {conteudo_json.get('email')}")
        if conteudo_json.get("status") == "recusado":
            print(f"Enviar Mensagem de Pagamento Recusado Para o Usuário {conteudo_json.get('email')}")
        if conteudo_json.get("status") == "reembolsado":
            print(f"Enviar Mensagem de Pagamento Reembolsado Para o Usuário {conteudo_json.get('email')}")
            print(f"Retirar Acesso do Usuário {conteudo_json.get('email')}")
        database.session.add(dado)
        database.session.commit()
    return "Teste"

@app.route("/historico", methods=['GET', 'POST'])
@login_required
def historico():
    email = request.args.get("busca")
    dados = Dados.query.filter(Dados.email == email).all()
    return render_template("historicodados.html", email = email, dados = enumerate(dados))
