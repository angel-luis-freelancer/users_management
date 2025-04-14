from flask import Blueprint

addresses_bp = Blueprint('addresses', __name__)

@addresses_bp.route('/')
def list_addresses():
    return {"message": "Lista de direcciones"}

