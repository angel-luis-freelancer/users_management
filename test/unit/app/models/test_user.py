import pytest
from uuid import uuid4
from app.models import User

class TestUserModel:
    def test_user_creation(self, db_session):
        user = User(
            uuid=str(uuid4()),
            first_name="Test",
            last_name="User",
            username="createtestuser",
            email="create_test@example.com"
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.uuid is not None
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.username == "createtestuser"
        assert user.email == "create_test@example.com"
        assert user.status == "pending"
        assert user.phone is None
        assert user.middle_name is None

    def test_required_fields(self, db_session):
        with pytest.raises(Exception):
            user = User()
            db_session.add(user)
            db_session.commit()

    def test_unique_constraints(self, db_session):
        user1 = User(
            uuid=str(uuid4()),
            first_name="User1",
            last_name="Test",
            username="uniqueuser",
            email="unique@mail.com"
        )
        db_session.add(user1)
        db_session.commit()
        
        with pytest.raises(Exception):
            user2 = User(
                uuid=str(uuid4()),
                first_name="User2",
                last_name="Test",
                username="uniqueuser",
                email="another@mail.com"
            )
            db_session.add(user2)
            db_session.commit()
            db_session.rollback()
        
        with pytest.raises(Exception):
            user3 = User(
                uuid=str(uuid4()),
                first_name="User3",
                last_name="Test",
                username="anotheruser",
                email="unique@mail.com"
            )
            db_session.add(user3)
            db_session.commit()
            db_session.rollback()

    def test_to_dict_method(self):
        user = User(
            uuid="123e4567-e89b-12d3-a456-426614174000",
            first_name="Dict",
            last_name="Test",
            username="dicttest",
            email="dict@example.com",
            status= 'active',
            phone="123456789",
            middle_name="Middle"
        )
        result = user.to_dict()
        expected = {
            'uuid': '123e4567-e89b-12d3-a456-426614174000',
            'first_name': 'Dict',
            'middle_name': 'Middle',
            'last_name': 'Test',
            'username': 'dicttest',
            'status': 'active',
            'email': 'dict@example.com',
            'phone': '123456789'
        }
        
        assert result == expected
        assert isinstance(result, dict)
