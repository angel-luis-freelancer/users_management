from .settings import Config, TestConfig
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    app.config.from_object(Config)
    db.init_app(app)
    return app

__all__ = ['Config', 'TestConfig', 'db', 'init_app']