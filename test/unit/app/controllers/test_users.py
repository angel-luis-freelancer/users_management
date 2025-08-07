import pytest
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from unittest.mock import patch

from app.controllers.users import UserController
from app.exceptions import (
    UserNotFoundException, 
    UserAlreadyExistsException, 
    InvalidUserDataException, 
    DatabaseException)
from app.models import User

class TestUserController:

    """
       __            __                __                         
      / /____  _____/ /_   ____ ____  / /_   __  __________  _____
     / __/ _ \/ ___/ __/  / __ `/ _ \/ __/  / / / / ___/ _ \/ ___/
    / /_/  __(__  ) /_   / /_/ /  __/ /_   / /_/ (__  )  __/ /    
    \__/\___/____/\__/   \__, /\___/\__/   \__,_/____/\___/_/     
                        /____/                                                                                 
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
        with pytest.raises(UserNotFoundException) as excinfo:
            UserController.get_user('username', 'nonexistent')

        assert excinfo.value.status_code == 404
        assert "username" in excinfo.value.message
        assert "nonexistent" in excinfo.value.message
        assert "not found" in excinfo.value.message

    def test_get_user_database_error(self, db_session):
        """Test para errores de base de datos"""
        with patch('app.controllers.users.db.session.execute') as mock_execute:
            mock_execute.side_effect = SQLAlchemyError("(pymysql.err.OperationalError) (1044, 'Access denied for user 'user'@'localhost' to database 'database_name'")
            with pytest.raises(DatabaseException) as excinfo:
                UserController.get_user('username', 'testuser')

            assert "Unknown error occurred" in str(excinfo.value)


    """
       __            __                          __                              
      / /____  _____/ /_   _____________  ____ _/ /____     __  __________  _____
     / __/ _ \/ ___/ __/  / ___/ ___/ _ \/ __ `/ __/ _ \   / / / / ___/ _ \/ ___/
    / /_/  __(__  ) /_   / /__/ /  /  __/ /_/ / /_/  __/  / /_/ (__  )  __/ /    
    \__/\___/____/\__/   \___/_/   \___/\__,_/\__/\___/   \__,_/____/\___/_/     
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
        with pytest.raises(KeyError):
            UserController.create_user({
                'first_name': 'Incomplete',
                'email': 'incomplete@example.com'
            })

    def test_create_user_duplicate_username(self, db_session):
        """Test para username duplicado"""
        user_data = {
            'first_name': 'Duplicate',
            'last_name': 'Username',
            'email': 'original@example.com'
        }
        UserController.create_user(user_data) 
        with pytest.raises(DatabaseException) as excinfo:
            UserController.create_user({
            'first_name': 'Duplicate',
            'last_name': 'Username',
            'email': 'other@example.com'
        })
        assert "Unknown error occurred" in str(excinfo.value)

    def test_create_user_duplicate_email(self, db_session):
        """Test para email duplicado"""
        user_data = {
            'first_name': 'Original',
            'last_name': 'User',
            'email': 'duplicate@example.com'
        }
        UserController.create_user(user_data)
        with pytest.raises(UserAlreadyExistsException) as excinfo:
            UserController.create_user({
                'first_name': 'Duplicate',
                'last_name': 'Email',
                'email': 'duplicate@example.com'
            })
        assert "already exists" in str(excinfo.value)
        assert "duplicate@example.com" in str(excinfo.value)

    def test_create_user_other_integrity_error(self, db_session):
        """Test para otros errores de integridad"""
        with patch('app.controllers.users.db.session.commit') as mock_commit:
            mock_commit.side_effect = IntegrityError("Simulated integrity error", None, None)
            with pytest.raises(DatabaseException) as excinfo:
                UserController.create_user({
                    'first_name': 'Test',
                    'last_name': 'Integrity',
                    'email': 'integrity@test.com'
                })

            assert "Simulated integrity error" in str(excinfo.value.details['original_error'])

    def test_create_user_general_database_error(self, db_session):
        """Test para otros errores de base de datos"""
        with patch('app.controllers.users.db.session.commit') as mock_commit:
            mock_commit.side_effect = SQLAlchemyError("Simulated database error")
            with pytest.raises(DatabaseException) as excinfo:
                UserController.create_user({
                    'first_name': 'Test',
                    'last_name': 'Error',
                    'email': 'error@test.com'
                })
            
            assert excinfo.value.details['original_error'] == "Simulated database error"


    """
       __            __                     __      __                              
      / /____  _____/ /_   __  ______  ____/ /___ _/ /____     __  __________  _____
     / __/ _ \/ ___/ __/  / / / / __ \/ __  / __ `/ __/ _ \   / / / / ___/ _ \/ ___/
    / /_/  __(__  ) /_   / /_/ / /_/ / /_/ / /_/ / /_/  __/  / /_/ (__  )  __/ /    
    \__/\___/____/\__/   \__,_/ .___/\__,_/\__,_/\__/\___/   \__,_/____/\___/_/     
                             /_/                                                    
    """

    def test_user_not_found(self, db_session):
        """Debe lanzar ValueError si no se encuentra el usuario"""
        with pytest.raises(UserNotFoundException) as excinfo:
            UserController.update_user("username", "fakeuser", {"first_name": "Nuevo"})

        assert excinfo.value.status_code == 404
        assert "username" in excinfo.value.message
        assert "fakeuser" in excinfo.value.message
        assert "not found" in excinfo.value.message

    def test_no_fields_to_update(self, db_session, sample_user):
        """Debe lanzar ValueError si no hay campos para actualizar"""
        same_data = {"first_name": sample_user.first_name}

        with pytest.raises(InvalidUserDataException) as excinfo:
            UserController.update_user("username", sample_user.username, same_data)

        assert excinfo.value.status_code == 400
        assert "username" in excinfo.value.message
        assert "No fields to update" in str(excinfo.value.message)
        assert sample_user.username in excinfo.value.message

    def test_successfull_update(self, db_session, sample_user):
        """Debe actualizar los campos correctamente"""
        new_data = {
            "first_name": "NuevoNombre",
            "middele_name": sample_user.middle_name
        }
        result = UserController.update_user("username", sample_user.username, new_data)
        updated_user = db_session.query(User).filter_by(username=sample_user.username).first()

        assert result["username"] == sample_user.username
        assert ("first_name", "NuevoNombre") in result["fields_updated"]
        assert updated_user.first_name == "NuevoNombre"

    def test_update_sqlalchemy_error(self, db_session, sample_user, monkeypatch):
        """Debe hacer rollback y lanzar ValueError si SQLAlchemy lanza un error"""
        def faulty_user_commit():
            raise SQLAlchemyError("DB exploded")

        monkeypatch.setattr("app.controllers.users.db.session.commit", faulty_user_commit)
        with pytest.raises(DatabaseException) as excinfo:
            UserController.update_user("username", sample_user.username, {"first_name": "Otro"})
        assert "DB exploded" in str(excinfo.value.details['original_error'])
    """
      ______          __                     __      __               __        __                
     /_  __/__  _____/ /_   __  ______  ____/ /___ _/ /____     _____/ /_____ _/ /___  _______    
      / / / _ \/ ___/ __/  / / / / __ \/ __  / __ `/ __/ _ \   / ___/ __/ __ `/ __/ / / / ___/    
     / / /  __(__  ) /_   / /_/ / /_/ / /_/ / /_/ / /_/  __/  (__  ) /_/ /_/ / /_/ /_/ (__  )     
    /_/  \___/____/\__/   \__,_/ .___/\__,_/\__,_/\__/\___/  /____/\__/\__,_/\__/\__,_/____/      
                              /_/                                                                 
    """

    def test_status_user_not_found(self, db_session):
        """Debe lanzar ValueError si no se encuentra el usuario"""
        with pytest.raises(UserNotFoundException) as excinfo:
            UserController.update_user_status("username", "fakeuser", {"first_name": "Nuevo"})

        assert excinfo.value.status_code == 404
        assert "username" in excinfo.value.message
        assert "fakeuser" in excinfo.value.message
        assert "not found" in excinfo.value.message

    def test_successful_update(self, db_session, sample_user):
        """Debe actualizar el status correctamente"""
        new_status = {'status': 'active'}
        result = UserController.update_user_status("username", sample_user.username, new_status)
        updated_user = db_session.query(User).filter_by(username=sample_user.username).first()

        assert result is None
        assert updated_user.status == new_status['status']

    def test_status_sqlalchemy_error(self, db_session, sample_user, monkeypatch):
        """Debe hacer rollback y lanzar ValueError si SQLAlchemy lanza un error"""
        def raise_db_error(*args, **kwargs):
            raise SQLAlchemyError ("Simulated DB error")

        monkeypatch.setattr(db_session, "commit", raise_db_error)
        with pytest.raises(DatabaseException) as excinfo:
            UserController.update_user_status("username", sample_user.username, {"status": "deleted"})
        assert "Simulated DB error" in str(excinfo.value.details['original_error'])