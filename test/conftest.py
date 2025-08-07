import pytest
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

from app.config import TestConfig
from app.decorators.users.query_params import validate_user_query_params
from app.handlers import setup_error_handlers
from app.models import db, User, Address
from app.routes import main_bp, api_bp
from app.exceptions.base import BaseAppException
from werkzeug.exceptions import InternalServerError

class CustomAppException(BaseAppException):
    def __init__(self, message="Custom error", status_code=418):
        super().__init__(message, status_code)

@pytest.fixture(scope='session')
def db_engine():
    engine = create_engine(TestConfig.SQLALCHEMY_DATABASE_URI)
    db.metadata.create_all(engine)
    yield engine
    db.metadata.drop_all(engine)
    engine.dispose()

@pytest.fixture
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=db_engine)
    session = Session()
    db.session = session
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope='module')
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/api')

    setup_error_handlers(app)

    @app.route("/raise-custom-error")
    def raise_custom_error():
        raise CustomAppException("This is a test error", status_code=418)

    @app.route("/test-method", methods=['GET'])
    def test_method():
        return jsonify({"ok": True})

    @app.route("/raise-500")
    def raise_500():
        raise Exception("Unexpected error")

    @app.route("/raise-internal")
    def raise_internal():
        raise InternalServerError("Simulated internal error")

    @app.route("/api/test-user-query/")
    @validate_user_query_params(['email'])
    def test_user_query(query_key, query_value):
        return jsonify({"message": "Success"}), 200

    yield app

@pytest.fixture(scope='module')
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_user_schema(monkeypatch):
    from unittest.mock import MagicMock
    mock_schema = MagicMock()
    mock_schema.model_dump.return_value = {}
    monkeypatch.setattr('app.schemas.user_schemas.CreateUserSchema', mock_schema)
    return mock_schema

@pytest.fixture()
def sample_user(db_session):
    unique_id = str(uuid4())
    user = User(
        uuid=unique_id,
        first_name='Sample',
        last_name='User',
        username=f'sampleuser{unique_id[:8]}',
        email=f'samplesample{unique_id[:8]}@sample.com',
        status='active'
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture()
def sample_address(db_session, sample_user):
    unique_id = str(uuid4())
    address = Address(
        uuid=unique_id,
        user_uuid=sample_user.uuid,
        street='Calle Falsa',
        number=123,
        city='Springfield',
        state='Illinois',
        country='USA',
        instructions='Casa azul con portón blanco'
    )
    db_session.add(address)
    db_session.commit()
    return address
