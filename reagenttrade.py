from flask import Flask, render_template, redirect, flash, abort, request, url_for
from tinydb import TinyDB, where, Query
from flask import Flask, render_template
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user
from flask.ext.sqlalchemy import SQLAlchemy
from Troca_form import Registrar_nova_troca
from flask.ext.login import UserMixin
import os


SECRET_KEY = 'yekterces'
SQLALCHEMY_DATABASE_URI = 'sqlite:///db/sql.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

UPLOAD_FOLDER = '/home/lucas/PycharmProjects/reagenttrade/static/produtos_figuras/'
ALLOWED_EXTENSIONS = set(['png'])

app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

db = SQLAlchemy(app)


#db = TinyDB('/home/lucas/PycharmProjects/reagenttrade/trocas.data')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

class Troca(db.Model):
    trade_id = db.Column(db.Integer, primary_key=True)
    produto = db.Column(db.String)
    usuario_nome = db.Column(db.String)
    quantidade = db.Column(db.Integer)
    foto_produto = db.Column(db.String)
    data_anuncio = db.Column(db.String)




@app.before_first_request
def init_request():
    db.create_all()


@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter_by(id=user_id)
    if user.count() == 1:
        return user.one()
    return None



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')


@app.route('/')
def index():
    return render_template('index.html')




@app.route('/cadastrar_troca', methods=['GET', 'POST'])
def cadastrar_troca():
    form = Registrar_nova_troca(request.form)
    for x in form:
        print x.data
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash("Foto selecionada")
        return render_template('nova_troca.html', form=form, figura_upload= 'static/produtos_figuras/' +filename)


    if request.method == 'POST' and form.validate():


        troca = Troca(
                      produto=form.produto.data,
                      usuario_nome=current_user.username,
                      quantidade=form.quantidade.data,
                      foto_produto='x',
                      data_anuncio='sem data ainda'
                      )

        db.session.add(troca)
        db.session.commit()

        flash('Troca cadastra')
        return redirect(url_for('trocas'))
    return render_template('nova_troca.html', form=form)



@app.route('/trocas')
def trocas():

    return render_template('trocas.html', mylist=[x for x in Troca.query.all()])



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['txtUsername'] # campos do register
        password = request.form['txtPassword']

        user =  User.query.filter_by(username=username)#procura na instancia de user a existencia de algum login semelhante
        if user.count() == 0: # se a quantidade for zero
            user = User(username=username, password=password) #cria a entrada
            db.session.add(user) #add user
            db.session.commit() #faz a modificacao

            flash('You have registered the username {0}. Please login'.format(username))
            return redirect(url_for('login'))
        else:
            print 'LOgin existente'
            flash('The username {0} is already in use.  Please try a new username.'.format(username))
            return redirect(url_for('register'))

    else:
        abort(405)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if request.method == 'GET':
            return render_template('login.html', next=request.args.get('next'))
    elif request.method == 'POST':
        username = request.form['txtUsername']
        password = request.form['txtPassword']

        user = User.query.filter_by(username=username).filter_by(password=password)
        if user.count() == 1:
            login_user(user.one())
            flash('Welcome back {0}'.format(username))
            try:
                next = request.form['next']
                return redirect(next)
            except:
                return redirect(url_for('index'))
        else:
            flash('Invalid login')
            return redirect(url_for('login'))
    else:
        return abort(405)





if __name__ == '__main__':
    app.debug = True
    app.run()
