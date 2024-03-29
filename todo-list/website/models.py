from website import db
from sqlalchemy.sql import func


# A Database model is like a blueprint for an object to work in your database.

class User(db.Model): # Nome da tabela
    # Colunas
    # id precisa ser uma PK
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(7), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)

    # Criando um constructor python
    def __init__(self, username, password):
        self.username = username
        self.password = password

        # Como vamos representar os usuarios?

    def __repr__(self):
        return f'<User: {self.username}'
    
class Todo(db.Model): # Nome da tabela
    # Colunas
    # id precisa ser uma PK
    id = db.Column(db.Integer, primary_key = True)
    # Criando um relacionamento 1 "usuario":n "notas"
    created_by= db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    title = db.Column(db.String(30), nullable = False)
    desc = db.Column(db.Text, nullable = False)
    state = db.Column(db.Boolean, default = False)
    #date = db.Column(db.DateTime(timezone=True), default=func.now())

    # Criando um constructor python
    def __init__(self, created_by, title, desc, state = False):
        self.created_by = created_by
        self.title = title
        self.desc = desc
        self.state = state

        # Como vamos representar os usuarios?

    def __repr__(self):
        return f'<User: {self.username}'