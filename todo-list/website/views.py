from flask import Blueprint, render_template, request, redirect, url_for, g
from website.auth import login_required
from .models import User,Todo
from website import db

# <variavel> = Instancia de Blueprint('<nome-da-instancia>')
views = Blueprint('views', __name__, url_prefix='/todo')



@views.route('/')
def index():
    return render_template("index.html")

@views.route('/list')
@login_required
def list():
    allnotes = Todo.query.all()
    return render_template("todo/list.html", allnotes = allnotes)

@views.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        function_title = request.form['title']
        function_desc = request.form['desc']

        obj_todo = Todo(g.user.id, function_title, function_desc)

        db.session.add(obj_todo)
        db.session.commit()
        return redirect(url_for('views.list'))

    return render_template("todo/create.html")

def get_todo(id):
    gettodo = Todo.query.get_or_404(id)
    return gettodo

@views.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):

    gettodoid = get_todo(id)

    if request.method == 'POST':
        gettodoid.title = request.form['title']
        gettodoid.desc = request.form['desc']
        gettodoid.state = True if request.form.get('state') == 'on' else False

        db.session.commit()
        return redirect(url_for('views.list'))
    
    return render_template("todo/update.html", todo = gettodoid)

@views.route('/delete/<int:id>')
@login_required
def delete(id):

    gettodoid = get_todo(id)   
    db.session.delete(gettodoid)
    db.session.commit()
    return redirect(url_for('views.list'))