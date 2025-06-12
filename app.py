from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import config

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'servidores.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Departamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    sigla = db.Column(db.String(20), nullable=False)
    departamento_superior = db.Column(db.String(120), nullable=False, default=config.DEPARTAMENTO_SUPERIOR)

    def __repr__(self):
        return f'<Departamento {self.nome}>'

class Servidor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(50), nullable=False)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'), nullable=False)
    departamento = db.relationship('Departamento', backref=db.backref('servidores', lazy=True))

    def __repr__(self):
        return f'<Servidor {self.nome}>'

# cria o banco de dados se ele ainda não existir
with app.app_context():
    db.create_all()
    # garante que o departamento raiz esteja presente no banco de dados
    if not Departamento.query.filter_by(nome=config.DEPARTAMENTO_SUPERIOR).first():
        root_dep = Departamento(
            nome=config.DEPARTAMENTO_SUPERIOR,
            sigla=config.DEPARTAMENTO_SUPERIOR,
            departamento_superior=config.DEPARTAMENTO_SUPERIOR,
        )
        db.session.add(root_dep)
        db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    departamentos = Departamento.query.all()
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        departamento_id = request.form['departamento_id']
        servidor = Servidor(nome=nome, email=email, telefone=telefone, departamento_id=departamento_id)
        db.session.add(servidor)
        db.session.commit()
        return redirect(url_for('listagem'))
    return render_template('cadastro.html', departamentos=departamentos)

@app.route('/listagem')
def listagem():
    servidores = Servidor.query.all()
    return render_template('listagem.html', servidores=servidores)


@app.route('/cadastro_departamento', methods=['GET', 'POST'])
def cadastro_departamento():
    departamentos = Departamento.query.filter(Departamento.nome != config.DEPARTAMENTO_SUPERIOR).all()
    if request.method == 'POST':
        nome = request.form['nome']
        sigla = request.form['sigla']
        superior_id = request.form['departamento_superior_id']
        if superior_id == 'root':
            departamento_superior = config.DEPARTAMENTO_SUPERIOR
        else:
            superior = Departamento.query.get(int(superior_id))
            departamento_superior = superior.nome if superior else config.DEPARTAMENTO_SUPERIOR
        departamento = Departamento(
            nome=nome,
            sigla=sigla,
            departamento_superior=departamento_superior,
        )
        db.session.add(departamento)
        db.session.commit()
        return redirect(url_for('listagem_departamentos'))
    return render_template(
        'cadastro_departamento.html',
        departamentos=departamentos,
        departamento_superior=config.DEPARTAMENTO_SUPERIOR,
    )


@app.route('/listagem_departamentos')
def listagem_departamentos():
    departamentos = Departamento.query.all()
    return render_template('listagem_departamentos.html', departamentos=departamentos)


@app.route('/organograma')
def organograma():
    departamentos = Departamento.query.all()
    servidores = Servidor.query.all()

    nodes = []

    # Add root department
    nodes.append({'name': config.DEPARTAMENTO_SUPERIOR, 'parent': ''})

    # Add departments
    for dep in departamentos:
        if dep.nome == config.DEPARTAMENTO_SUPERIOR:
            continue
        parent = dep.departamento_superior if dep.departamento_superior != dep.nome else config.DEPARTAMENTO_SUPERIOR
        nodes.append({'name': dep.nome, 'parent': parent})

    # Add servers
    for servidor in servidores:
        nodes.append({'name': servidor.nome, 'parent': servidor.departamento.nome})

    return render_template('organograma.html', nodes=nodes)

if __name__ == '__main__':
    app.run(debug=True)
