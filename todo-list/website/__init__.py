from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # The object that will be used for requests
DB_NAME = "secflaskapp.db"

def create_app():
    app = Flask(__name__)

    # Configuracao do projeto
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)

    # Registrar Blueprint
    from .views import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    from .models import User, Todo

    # Import models that may be missing
    with app.app_context():
        db.create_all()

    return app