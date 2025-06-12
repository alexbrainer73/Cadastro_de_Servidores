from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'servidores.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Servidor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Servidor {self.nome}>'

# cria o banco de dados se ele ainda não existir
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        servidor = Servidor(nome=nome, email=email, telefone=telefone)
        db.session.add(servidor)
        db.session.commit()
        return redirect(url_for('listagem'))
    return render_template('cadastro.html')

@app.route('/listagem')
def listagem():
    servidores = Servidor.query.all()
    return render_template('listagem.html', servidores=servidores)

if __name__ == '__main__':
    app.run(debug=True)
