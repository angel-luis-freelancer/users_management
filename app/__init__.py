from flask import Flask
from sqlalchemy.orm import scoped_session, sessionmaker

from .config import db, init_app
from .routes import main_bp, api_bp

def create_app(config_class=None):
    app = Flask(__name__)
    if config_class:
        app.config.from_object(config_class)
    else:
        from app.config.settings import Config
        app.config.from_object(Config)

    init_app(app)

    with app.app_context():
        db.session = scoped_session(
            sessionmaker(
                bind=db.engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False
            )
        )
    
    # Configuración de manejo automático de sesiones
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """Cierra la sesión al finalizar cada request"""
        db.session.remove()

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app