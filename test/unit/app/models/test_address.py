import pytest
from uuid import uuid4
from app.models import Address, User

class TestAddressModel:
    def test_address_creation(self, db_session):
        user = User(
            uuid=str(uuid4()),
            first_name="Test",
            last_name="User",
            username="testuser",
            email="test@example.com"
        )
        db_session.add(user)
        db_session.commit()

        address = Address(
            uuid=str(uuid4()),
            user_uuid=user.uuid,
            street="123 Main St",
            number=42,
            city="Testville",
            state="Test State",
            country="Test Country"
        )
        db_session.add(address)
        db_session.commit()
        
        assert address.uuid is not None
        assert address.user_uuid == user.uuid
        assert address.street == "123 Main St"
        assert address.number == 42
        assert address.city == "Testville"
        assert address.state == "Test State"
        assert address.country == "Test Country"
        assert address.instructions is None 

    def test_to_dict_method(self, db_session):
        user = User(
            uuid=str(uuid4()),
            first_name="Dict",
            last_name="Test",
            username="dicttest",
            email="dict@example.com"
        )
        db_session.add(user)
        db_session.commit()

        address = Address(
            uuid="123e4567-e89b-12d3-a456-426614174000",
            user_uuid=user.uuid,
            street="789 Dict St",
            number=123,
            city="Dict City",
            state="Dict State",
            country="Dict Country",
            instructions="Ring the bell"
        )
        
        result = address.to_dict()
        
        expected = {
            'uuid': '123e4567-e89b-12d3-a456-426614174000',
            'user_uuid': user.uuid,
            'street': '789 Dict St',
            'number': 123,
            'city': 'Dict City',
            'state': 'Dict State',
            'country': 'Dict Country',
            'instructions': 'Ring the bell'
        }
        
        assert result == expected
        assert isinstance(result, dict)

    def test_user_relationship(self, db_session):
        user = User(
            uuid=str(uuid4()),
            first_name="Relation",
            last_name="Test",
            username="reltest",
            email="relation@example.com"
        )
        
        address = Address(
            uuid=str(uuid4()),
            street="101 Relation Rd",
            number=1,
            city="Relation City",
            state="Relation State",
            country="Relation Country",
            user=user 
        )
        db_session.add_all([user, address])
        db_session.commit()
        
        assert address.user == user
        assert user.addresses.count() == 1
        assert user.addresses.first().street == "101 Relation Rd"

