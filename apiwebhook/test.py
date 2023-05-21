from apiwebhook import app, database
from apiwebhook.models import Users, Dados

# with app.app_context():
#     database.drop_all()
#     database.create_all()

with app.app_context():
    a =Dados.query.filter(Dados.email == 'Trivedi27@omega.com').all()
    primeiro_dado = a[0]  # Acessa o primeiro elemento da lista
    nome = primeiro_dado.nome
    print(nome)