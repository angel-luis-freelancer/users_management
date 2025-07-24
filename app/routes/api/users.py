from flask import Blueprint, jsonify, request

from ...controllers import UserController
from ...decorators import validate_user_query_params, validate_body
from ...schemas import CreateUserSchema, UpdateUserSchema

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@validate_user_query_params(['username', 'email'])
def get_user(query_key, query_value):
    try:
        data = UserController.get_user(query_key, query_value)
        return jsonify(data), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@users_bp.route('/', methods=['POST'])
@validate_body(CreateUserSchema)
def create_user():
    try:
        user = UserController.create_user(request.validated_data.model_dump())
        return jsonify(user), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@users_bp.route('/update', methods=['PATCH'])
@validate_user_query_params(['username', 'email'])
@validate_body(UpdateUserSchema)
def update_user(query_key, query_value):
    try:
        response = UserController.update_user(query_key, query_value, request.validated_data.model_dump())
        return jsonify(response), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400