from flask import render_template, request, redirect, url_for, current_app
# Assuming db instance is initialized in app.py and passed or models.py is adjusted
from models import db, Departamento, Servidor
import config

def register_routes(app):
    @app.route('/')
    def index():
        num_servers = Servidor.query.count()
        num_departments = Departamento.query.count()
        return render_template('index.html', num_servers=num_servers, num_departments=num_departments)

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
