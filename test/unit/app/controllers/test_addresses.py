import pytest

from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import patch
from uuid import uuid4

from app.controllers.addresses import AddressController
from app.exceptions import UserNotFoundException, DatabaseException
from app.models import Address

class TestAddressController:

    """
       __            __                __               __    __                   
      / /____  _____/ /_   ____ ____  / /_   ____ _____/ /___/ /_______  __________
     / __/ _ \/ ___/ __/  / __ `/ _ \/ __/  / __ `/ __  / __  / ___/ _ \/ ___/ ___/
    / /_/  __(__  ) /_   / /_/ /  __/ /_   / /_/ / /_/ / /_/ / /  /  __(__  |__  ) 
    \__/\___/____/\__/   \__, /\___/\__/   \__,_/\__,_/\__,_/_/   \___/____/____/  
                        /____/                                                     
    """
        
    @pytest.mark.parametrize(
    "key, value_getter",
    [
        ("email", lambda user: user.email),
        ("username", lambda user: user.username),
    ]
)
    def test_get_user_address_success(db_session, sample_user, sample_address, key, value_getter):
        """Test: Obtener direcciones del usuario - Casos exitosos por email y username"""
        value = value_getter(sample_user)
        result = AddressController.get_user_address(key, value)

        assert isinstance(result, dict)
        assert len(result) == 2
        assert result['metadata']['username'] == sample_user.username
        assert result['addresses'][0]['street'] == 'Calle Falsa'
        assert result['addresses'][0]['number'] == 123
        assert result['addresses'][0]['city'] == 'Springfield'
        assert result['addresses'][0]['state'] == 'Illinois'
        assert result['addresses'][0]['country'] == 'USA'
        assert result['addresses'][0]['instructions'] == 'Casa azul con portón blanco'

    def test_get_user_address_multiple_addresses(self, db_session, sample_user, sample_address):
        """Test: Usuario con múltiples direcciones"""
        address2_uuid = str(uuid4())
        address2 = Address(
            uuid=address2_uuid,
            user_uuid=sample_user.uuid,
            street='Avenida Principal',
            number=456,
            city='Capital',
            state='Madrid',
            country='España',
            instructions='Edificio moderno'
        )
        db_session.add(address2)
        db_session.commit() # Crear segunda dirección
        result = AddressController.get_user_address('email', sample_user.email)
        streets = [addr['street'] for addr in result['addresses']]

        assert len(streets) == 2
        assert sample_address.street and 'Avenida Principal' in streets

    def test_get_user_address_no_addresses(self, db_session, sample_user):
        """Test: Usuario sin direcciones"""
        result = AddressController.get_user_address('email', sample_user.email)
        assert isinstance(result, dict)
        assert len(result) == 2
        assert len(result['addresses']) == 0

    @patch('app.models.db.session.execute')
    def test_get_user_address_database_error(self, mock_execute, db_session):
        """Test: Error de base de datos"""
        mock_execute.side_effect = SQLAlchemyError("Database connection error")
        with pytest.raises(DatabaseException) as excinfo:
            AddressController.get_user_address('email', 'test@test.com')

        assert "Unknown error occurred" in str(excinfo.value)
        assert excinfo.value.details['original_error'] == "Database connection error"

    """
       __            __                          __                    __    __                   
      / /____  _____/ /_   _____________  ____ _/ /____     ____ _____/ /___/ /_______  __________
     / __/ _ \/ ___/ __/  / ___/ ___/ _ \/ __ `/ __/ _ \   / __ `/ __  / __  / ___/ _ \/ ___/ ___/
    / /_/  __(__  ) /_   / /__/ /  /  __/ /_/ / /_/  __/  / /_/ / /_/ / /_/ / /  /  __(__  |__  ) 
    \__/\___/____/\__/   \___/_/   \___/\__,_/\__/\___/   \__,_/\__,_/\__,_/_/   \___/____/____/  
                                                                                                
    """

    @patch('app.controllers.addresses.UserController.get_user')
    def test_create_address_success(self, mock_get_user, db_session, sample_user):
        """Test: Crear dirección exitosamente"""
        mock_get_user.return_value = { # Mock del usuario existente
            'uuid': sample_user.uuid,
            'username': sample_user.username,
            'email': sample_user.email
        }
        address_data = {
            'street': 'Nueva Calle',
            'number': 789,
            'city': 'Nueva Ciudad',
            'state': 'Nuevo Estado',
            'country': 'Nuevo País',
            'instructions': 'Casa nueva'
        }
        result = AddressController.create_address('email', sample_user.email, address_data)
        
        assert result is not None
        assert isinstance(result, dict)
        assert result['street'] == 'Nueva Calle'
        assert result['number'] == 789
        assert result['city'] == 'Nueva Ciudad'
        assert result['state'] == 'Nuevo Estado'
        assert result['country'] == 'Nuevo País'
        assert result['instructions'] == 'Casa nueva'
        assert result['username'] == sample_user.username
        mock_get_user.assert_called_once_with('email', sample_user.email) # Verificar que se llamó al UserController


    @patch('app.controllers.addresses.UserController.get_user')
    @patch('app.models.db.session.commit')
    def test_create_address_sqlalchemy_error(self, mock_commit, mock_get_user, db_session, sample_user):
        """Test: Error general de SQLAlchemy"""
        mock_get_user.return_value = {
            'uuid': sample_user.uuid,
            'email': sample_user.email
        }
        mock_commit.side_effect = SQLAlchemyError("Database error")
        
        address_data = {
            'street': 'Test Street',
            'number': 123,
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'instructions': 'Test instructions'
        }
        with pytest.raises(DatabaseException) as excinfo:
            AddressController.create_address('email', sample_user.email, address_data)

        assert "Unknown error occurred" in str(excinfo.value)
        assert excinfo.value.details['original_error'] == "Database error"