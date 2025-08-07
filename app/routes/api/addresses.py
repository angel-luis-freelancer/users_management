from flask import Blueprint, request

from ...controllers import AddressController
from ...decorators import validate_user_query_params, validate_body
from ...schemas import CreateAddressSchema

addresses_bp = Blueprint('addresses', __name__)

@addresses_bp.route('/user', methods=['GET'])
@validate_user_query_params(['username', 'email'])
def get_users_address(query_key, query_value):
    data = AddressController.get_user_address(query_key, query_value)
    return data, 200
@addresses_bp.route('/', methods=['POST'])
@validate_user_query_params(['username', 'email'])
@validate_body(CreateAddressSchema)
def create_address(query_key, query_value):
    data = AddressController.create_address(query_key, query_value, request.validated_data.model_dump())
    return data, 200
