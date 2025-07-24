import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.controllers.addresses import AddressController
from app.models import Address

class TestAddressController:
    def test_get_user_address_by_email_success(self, db_session, sample_user, sample_address):
        """Test: Obtener direcciones por email - Caso exitoso"""
        result = AddressController.get_user_address('email', sample_user.email)
        assert isinstance(result, dict)
        assert len(result) == 2
        assert result['metadata']['username'] == sample_user.username
        assert result['addresses'][0]['street'] == 'Calle Falsa'
        assert result['addresses'][0]['number'] == 123
        assert result['addresses'][0]['city'] == 'Springfield'
        assert result['addresses'][0]['state'] == 'Illinois'
        assert result['addresses'][0]['country'] == 'USA'
        assert result['addresses'][0]['instructions'] == 'Casa azul con portón blanco'

    def test_get_user_address_by_username_success(self, db_session, sample_user, sample_address):
        """Test: Obtener direcciones por username - Caso exitoso"""
        result = AddressController.get_user_address('username', sample_user.username)
        assert isinstance(result, dict)
        assert len(result) == 2
        assert result['metadata']['username'] == sample_user.username
        assert result['addresses'][0]['street'] == 'Calle Falsa'
        assert result['addresses'][0]['number'] == 123
        assert result['addresses'][0]['city'] == 'Springfield'
        assert result['addresses'][0]['state'] == 'Illinois'
        assert result['addresses'][0]['country'] == 'USA'
        assert result['addresses'][0]['instructions'] == 'Casa azul con portón blanco'

    def test_get_user_address_multiple_addresses(self, db_session, sample_user):
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
        
        # assert len(result) == 2
        streets = [addr['street'] for addr in result['addresses']]
        # assert 'Calle Falsa' in streets
        assert 'Avenida Principal' in streets

    def test_get_user_address_no_addresses(self, db_session, sample_user):
        """Test: Usuario sin direcciones"""
        result = AddressController.get_user_address('email', sample_user.email) # No crear sample_address fixture
        assert isinstance(result, dict)
        assert len(result) == 2
        assert len(result['addresses']) == 0

    @patch('app.models.db.session.execute')
    def test_get_addresses_user_dosent_exist(self, mock_execute, db_session):
        """Test: El usuario no existe"""
        with patch('app.models.db.session.execute') as mock_execute:
            mock_execute.return_value.scalar_one_or_none.return_value = None
            with pytest.raises(ValueError) as excinfo:
                AddressController.get_user_address('email', 'test@example.com')
            
            assert "User with email = test@example.com dosent exist" in str(excinfo.value)

    @patch('app.models.db.session.execute')
    def test_get_user_address_database_error(self, mock_execute, db_session):
        """Test: Error de base de datos"""
        mock_execute.side_effect = SQLAlchemyError("Database connection error")
        with pytest.raises(ValueError, match="Error getting the address"):
            AddressController.get_user_address('email', 'test@test.com')

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
    def test_create_address_user_not_found(self, mock_get_user, db_session):
        """Test: Usuario no encontrado"""
        mock_get_user.return_value = None
        address_data = {
            'street': 'Test Street',
            'number': 123,
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'instructions': 'Test instructions'
        }
        with pytest.raises(ValueError) as excinfo:
            AddressController.create_address('email', 'noexiste@test.com', address_data)

        assert 'User with email = noexiste@test.com dosent exist' in str(excinfo.value)

    @patch('app.controllers.addresses.UserController.get_user')
    def test_create_address_missing_required_fields(self, mock_get_user, db_session, sample_user):
        """Test: Error por campos faltantes"""
        mock_get_user.return_value = {
            'uuid': sample_user.uuid,
            'email': sample_user.email
        }
        # address_data incompleto
        address_data = {
            'street': 'Test Street',
            'number': 123
            # faltan: city, state, country, instructions
        }
        with pytest.raises(KeyError):
            AddressController.create_address('email', sample_user.email, address_data)


    @patch('app.controllers.addresses.UserController.get_user')
    @patch('app.models.db.session.commit')
    def test_create_address_integrity_error(self, mock_commit, mock_get_user, db_session, sample_user):
        """Test: Error de integridad de base de datos"""
        mock_get_user.return_value = {
            'uuid': sample_user.uuid,
            'email': sample_user.email
        }
        mock_commit.side_effect = IntegrityError("statement", "params", "orig")
        
        address_data = {
            'street': 'Test Street',
            'number': 123,
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'instructions': 'Test instructions'
        }
        with pytest.raises(ValueError, match="Database integrity error"):
            AddressController.create_address('email', sample_user.email, address_data)

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
        
        with pytest.raises(ValueError, match="Error creating the address"):
            AddressController.create_address('email', sample_user.email, address_data)

    @patch('app.controllers.addresses.UserController.get_user')
    def test_create_address_with_empty_instructions(self, mock_get_user, db_session, sample_user):
        """Test: Crear dirección con instrucciones vacías"""
        mock_get_user.return_value = {
            'uuid': sample_user.uuid,
            'username': sample_user.username,
            'email': sample_user.email
        }
        
        address_data = {
            'street': 'Test Street',
            'number': '123',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'instructions': ''  # Instrucciones vacías
        }
        
        result = AddressController.create_address('email', sample_user.email, address_data)
        
        assert result is not None
        assert result['instructions'] == ''

    @patch('app.controllers.addresses.UserController.get_user')
    def test_create_address_with_username_key(self, mock_get_user, db_session, sample_user):
        """Test: Crear dirección usando username como key"""
        mock_get_user.return_value = {
            'uuid': sample_user.uuid,
            'username': sample_user.username
        }
        
        address_data = {
            'street': 'Username Street',
            'number': '999',
            'city': 'Username City',
            'state': 'Username State',
            'country': 'Username Country',
            'instructions': 'Username test'
        }
        
        result = AddressController.create_address('username', sample_user.username, address_data)
        
        assert result is not None
        assert result['street'] == 'Username Street'
        mock_get_user.assert_called_once_with('username', sample_user.username)