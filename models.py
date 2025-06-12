from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()

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
