import pytest
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from uuid import uuid4
from unittest.mock import patch
from app.controllers.users import UserController
from app.models import User

class TestUserController:

    """
    ___ ___ _____   _   _ ___ ___ ___   _____ ___ ___ _____ 
    / __| __|_   _| | | | / __| __| _ \ |_   _| __/ __|_   _|
    | (_ | _|  | |   | |_| \__ \ _||   /   | | | _|\__ \ | |  
    \___|___| |_|    \___/|___/___|_|_\   |_| |___|___/ |_|                                                
    """

    def test_get_user_success_by_username(self, db_session, sample_user):
        result = UserController.get_user('username', sample_user.username)
        assert result is not None
        assert result['username'] == sample_user.username
        assert result['email'] == sample_user.email
        assert result['uuid'] == sample_user.uuid

    def test_get_user_success_by_email(self, db_session, sample_user):
        result = UserController.get_user('email', sample_user.email)
        assert result is not None
        assert result['username'] == sample_user.username
        assert result['email'] == sample_user.email
        assert result['uuid'] == sample_user.uuid

    def test_get_user_not_found(self, db_session):
        """Test cuando el usuario no existe"""
        result = UserController.get_user('username', 'nonexistent')
        assert result is None

    def test_get_user_database_error(self, db_session):
        """Test para errores de base de datos"""
        with patch('app.controllers.users.db.session.execute') as mock_execute:
            mock_execute.side_effect = SQLAlchemyError("Simulated database error")
            
            with pytest.raises(ValueError) as excinfo:
                UserController.get_user('username', 'testuser')
            assert "Error getting user" in str(excinfo.value)


    """
    ___ ___ ___   _ _____ ___   _   _ ___ ___ ___   _____ ___ ___ _____ 
    / __| _ \ __| /_\_   _| __| | | | / __| __| _ \ |_   _| __/ __|_   _|
    | (__|   / _| / _ \| | | _|  | |_| \__ \ _||   /   | | | _|\__ \ | |  
    \___|_|_\___/_/ \_\_| |___|  \___/|___/___|_|_\   |_| |___|___/ |_|  
    """

    def test_create_user_success(self, db_session):
        """Test caso exitoso para creación de usuario"""
        user_data = {
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'phone': '1234567890'
        }
        
        result = UserController.create_user(user_data)
        assert result is not None
        assert result['first_name'] == 'New'
        assert result['last_name'] == 'User'
        assert result['username'] == 'newuser'
        assert result['email'] == 'new@example.com'
        assert result['status'] == 'active'

    def test_create_user_missing_required_fields(self, db_session):
        """Test cuando faltan campos requeridos"""
        # Falta last_name
        with pytest.raises(KeyError):
            UserController.create_user({
                'first_name': 'Incomplete',
                'email': 'incomplete@example.com'
            })

    def test_create_user_duplicate_username(self, db_session):
        """Test para username duplicado"""
        # Crear usuario inicial
        user_data = {
            'first_name': 'Duplicate',
            'last_name': 'Username',
            'email': 'original@example.com'
        }
        UserController.create_user(user_data) 
        
        with pytest.raises(ValueError) as excinfo:
            UserController.create_user({
            'first_name': 'Duplicate',
            'last_name': 'Username',
            'email': 'other@example.com'
        })
        assert "The username already exists" in str(excinfo.value)

    def test_create_user_duplicate_email(self, db_session):
        """Test para email duplicado"""
        # Crear usuario inicial
        user_data = {
            'first_name': 'Original',
            'last_name': 'User',
            'email': 'duplicate@example.com'
        }
        UserController.create_user(user_data)
        
        # Intentar crear usuario con mismo email
        with pytest.raises(ValueError) as excinfo:
            UserController.create_user({
                'first_name': 'Duplicate',
                'last_name': 'Email',
                'email': 'duplicate@example.com'
            })
        assert "The email already exists" in str(excinfo.value)

    def test_create_user_other_integrity_error(self, db_session):
        """Test para otros errores de integridad"""
        with patch('app.controllers.users.db.session.commit') as mock_commit:
            mock_commit.side_effect = IntegrityError("Simulated integrity error", None, None)
            
            with pytest.raises(ValueError) as excinfo:
                UserController.create_user({
                    'first_name': 'Test',
                    'last_name': 'Integrity',
                    'email': 'integrity@test.com'
                })
            assert "Database integrity error" in str(excinfo.value)

    def test_create_user_general_database_error(self, db_session):
        """Test para otros errores de base de datos"""
        with patch('app.controllers.users.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Simulated database error")
            
            with pytest.raises(ValueError) as excinfo:
                UserController.create_user({
                    'first_name': 'Test',
                    'last_name': 'Error',
                    'email': 'error@test.com'
                })
            
            assert "Error creating the user" in str(excinfo.value)