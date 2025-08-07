from flask import Blueprint, jsonify, request

from ...controllers import UserController
from ...decorators import validate_user_query_params, validate_body
from ...schemas import CreateUserSchema, UpdateUserSchema, UpdateStatusUserSchema

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@validate_user_query_params(['username', 'email'])
def get_user(query_key, query_value):
    response = UserController.get_user(query_key, query_value)
    return jsonify(response), 200

@users_bp.route('/', methods=['POST'])
@validate_body(CreateUserSchema)
def create_user():
    response = UserController.create_user(request.validated_data.model_dump())
    return jsonify(response), 201
    
@users_bp.route('/update/', methods=['PATCH'])
@validate_user_query_params(['username', 'email'])
@validate_body(UpdateUserSchema)
def update_user(query_key, query_value):
    response = UserController.update_user(query_key, query_value, request.validated_data.model_dump())
    return jsonify(response), 200
    
@users_bp.route('/status/', methods=['PATCH'])
@validate_user_query_params(['username', 'email'])
@validate_body(UpdateStatusUserSchema)
def update_user_status(query_key, query_value):
    response = UserController.update_user_status(query_key, query_value, request.validated_data.model_dump())
    return jsonify(response), 204