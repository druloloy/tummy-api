from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_compress import Compress
from config import config
from flask_cors import CORS
from os import environ
db = SQLAlchemy()

def create_app(key: str):
    app = Flask(__name__)
    app.config.from_object(config[key])
    
    db.init_app(app)
    Compress(app)
    Migrate(app, db)
    CORS(app, origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ])

    blueprint = Blueprint('api_version1', __name__, url_prefix='/api/v1')

    from apps.register import register_routes
    register_routes(blueprint)

    app.register_blueprint(blueprint)

    return app