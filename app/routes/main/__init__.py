from flask import Blueprint
from .root import root_bp

# Blueprint padre para API
main_bp = Blueprint('home', __name__)

main_bp.register_blueprint(root_bp, url_prefix='/')

__all__ = ['main_bp']