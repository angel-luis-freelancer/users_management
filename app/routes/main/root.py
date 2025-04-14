from flask import Blueprint

root_bp = Blueprint('main', __name__)

@root_bp.route('/ping')
def ping():
    return 'pong'

