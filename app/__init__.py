import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Garante que a pasta instance/ existe
    os.makedirs(app.instance_path, exist_ok=True)

    # Caminho correto para o banco SQLite
    db_path = os.path.join(app.instance_path, 'db.sqlite')
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importa os modelos (depois de db.init_app)
    from app import models

    # Blueprint de autenticação
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Blueprint da parte principal
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Cria as tabelas
    with app.app_context():
        db.create_all()

    return app



