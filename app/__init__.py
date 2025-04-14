from flask import Flask
from .config import init_app

from .routes import main_bp, api_bp

def create_app(config_class=None):
    app = Flask(__name__)
    if config_class:
        app.config.from_object(config_class)
    else:
        from app.config.settings import Config
        app.config.from_object(Config)

    app = init_app(app)
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app