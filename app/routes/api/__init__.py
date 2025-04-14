from flask import Blueprint
from .users import users_bp
from .addresses import addresses_bp

# Blueprint padre para API
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Registrar blueprints hijos
api_bp.register_blueprint(users_bp, url_prefix='/users')
api_bp.register_blueprint(addresses_bp, url_prefix='/addresses')

__all__ = ['api_bp']