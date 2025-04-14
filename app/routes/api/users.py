from flask import Blueprint, jsonify, request

from ...controllers import UserController
from ...decorators import validate_query_params, validate_body
from ...schemas import UserCreateSchema

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@validate_query_params(['username', 'uuid', 'email'])
def get_user():
    params = dict(request.args)
    if len(params) > 1:
        return jsonify({"error": "too many parameters, only admited 1"}), 400
    
    key = list(params.keys())[0] 
    value = params[key]
    data = UserController.get_user(key, value)
    return jsonify(data), 200


@users_bp.route('/', methods=['POST'])
@validate_body(UserCreateSchema)
def create_user():
    try:
        user = UserController.create_user(request.validated_data.model_dump())
        return jsonify(user), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400