from flask import Blueprint, jsonify, request

from ...controllers import AddressController
from ...decorators import validate_query_params, validate_body
from ...schemas import CreateAddressSchema

addresses_bp = Blueprint('addresses', __name__)

@validate_query_params(['username', 'email'])
@addresses_bp.route('/user', methods=['GET'])
def get_users_address():
    try:
        params = dict(request.args)
        if len(params) > 1:
            raise ValueError("too many parameters, only admited 1")
        
        if len(params) == 0:
            raise ValueError("we need the parameters email or username")
        
        key = list(params.keys())[0]
        value = params[key]
        data = AddressController.get_user_address(key, value)
        return data, 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@validate_query_params(['username', 'uuid', 'email'])
@addresses_bp.route('/', methods=['POST'])
@validate_body(CreateAddressSchema)
def create_address():
    try:
        params = dict(request.args)
        if len(params) > 1:
            raise ValueError("too many parameters, only admited 1")
        
        if len(params) == 0:
            raise ValueError("we need the parameters email or username")
        
        key = list(params.keys())[0]
        value = params[key]
        data = AddressController.create_address(key, value, request.validated_data.model_dump())
        return data, 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400