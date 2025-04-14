import pytest
from app.models import User, Address

def test_user_creation(db_session, user_factory):
    user = user_factory(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com"
    )
    assert user.uuid is not None
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.status == "active"
    
    db_user = db_session.query(User).filter_by(email="john.doe@example.com").first()
    assert db_user is not None
    assert db_user.username == user.username

def test_user_email_uniqueness(db_session, user_factory):
    user_factory(email="unique@example.com")
    with pytest.raises(Exception):
        user_factory(email="unique@example.com")
