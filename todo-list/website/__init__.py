from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # The object that will be used for requests
DB_NAME = "mydb.db"

def create_app():
    myapp = Flask(__name__)

    # Configuracao do projeto
    myapp.config['SECRET_KEY'] = 'qiwuyeiweyq ywqiey'
    myapp.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(myapp)

    # Registrar Blueprint
    from .views import views
    from .auth import auth

    myapp.register_blueprint(views)
    myapp.register_blueprint(auth)

    from .models import User, Todo

    # Import models that may be missing
    with myapp.app_context():
        db.create_all()

    return myapp