from flask import Flask, render_template, request, redirect, session, url_for
from flask import flash
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = 'Alura'

app.config['SQLALCHEMY_DATABASE_URI'] = '{SGB}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGB='mysql+mysqlconnector',
    usuario='root',
    senha='root',
    servidor='localhost',
    database='jogoteca'
    )

db = SQLAlchemy(app)

class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.nome

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True, nullable=False)
    nome = db.Column(db.String(20), primary_key=True, nullable=False)
    senha = db.Column(db.String(100), primary_key=True, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.nome

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Você precisa fazer login para adicionar um novo jogo!')
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    
    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já cadastrado!')
        return redirect(url_for('index'))
    
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()


    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():

    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()

    if usuario:
        
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário ou senha inválidos!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário deslogado com sucesso!')
    return redirect(url_for('index'))

app.run(debug=True)