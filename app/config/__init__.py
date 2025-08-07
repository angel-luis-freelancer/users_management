from flask_sqlalchemy import SQLAlchemy

from .settings import Config, TestConfig
from .logging import setup_logging
db = SQLAlchemy()

def init_app(app):
    if 'SQLALCHEMY_DATABASE_URI' not in app.config:
        app.config.from_object(Config)
    db.init_app(app)
    return app

__all__ = ['Config', 'db', 'init_app', 'setup_logging', 'TestConfig']