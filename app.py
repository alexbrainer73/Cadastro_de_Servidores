from flask import Flask
import os
import config

# Import db instance from models.py
from models import db, Departamento, Servidor
# Import routes
from routes import register_routes

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'servidores.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db.init_app(app)

# Register routes
register_routes(app)

# Create database tables and initial data
with app.app_context():
    db.create_all()
    # Garante que o departamento raiz esteja presente no banco de dados
    if not Departamento.query.filter_by(nome=config.DEPARTAMENTO_SUPERIOR).first():
        root_dep = Departamento(
            nome=config.DEPARTAMENTO_SUPERIOR,
            sigla=config.DEPARTAMENTO_SUPERIOR,
            departamento_superior=config.DEPARTAMENTO_SUPERIOR, # Auto-referência para o superior, se for o mesmo
        )
        db.session.add(root_dep)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
