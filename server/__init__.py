import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__.split('.')[0])
    cfg = config or os.getenv('APP_SETTINGS')
    app.config.from_object(cfg)
    db.init_app(app)

    from .api.views import user_routes
    app.register_blueprint(user_routes)
    return app
