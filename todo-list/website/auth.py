from flask import (
    Blueprint, render_template, request, url_for, redirect, flash, session, g
    )

# the g will be used to keep a value along the whole app

from werkzeug.security import generate_password_hash, check_password_hash


from .models import User,Todo
from website import db

auth = Blueprint('auth', __name__,url_prefix='/todo')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username, generate_password_hash(password))

        error = None

        #Buscar um nome de usuario, filtrando um dado de acordo como colocamos
        user_name = User.query.filter_by(username = username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        
        else:
            error = f'The user {username} already exists'
        
        flash(error)
        
    return render_template('auth/register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        # Validar dados, usuario e senha
        user = User.query.filter_by(username = username).first()
        if user == None:
            error = 'Username is incorrect'
        elif not check_password_hash(user.password, password):
            error = 'Bad password'
        
        # Start sesion/login
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('views.list'))
        
        else:
            error = f'The user {username} already exists'
        
        flash(error)

    return render_template('auth/login.html')

@auth.before_app_request
# Keeping session
def load_logged_user():
    user_id = session.get('user_id') # get['user_id] related to the session['user_id']
    
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.index'))

# Fazer a view de '/list' esteja disponivel somente com sessao aberta/feito login
import functools
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view