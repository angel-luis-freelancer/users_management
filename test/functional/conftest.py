import pytest
from faker import Faker
from sqlalchemy.orm import sessionmaker
from app.models import User, Address
@pytest.fixture
def fake():
    return Faker()

@pytest.fixture
def user_factory(db_session, fake):
    def _user_factory(**kwargs):
        user = User(
            uuid=fake.uuid4(),
            first_name=kwargs.get('first_name', fake.first_name()),
            middle_name=kwargs.get('middle_name', fake.first_name()),
            last_name=kwargs.get('last_name', fake.last_name()),
            username=kwargs.get('username', fake.user_name()),
            status=kwargs.get('status', 'active'),
            email=kwargs.get('email', fake.email()),
            phone=kwargs.get('phone', fake.phone_number())
        )
        db_session.add(user)
        db_session.commit()
        return user
    return _user_factory

@pytest.fixture
def address_factory(db_session, fake):
    def _address_factory(**kwargs):
        address = Address(
            uuid=fake.uuid4(),
            street=kwargs.get('street', fake.street_name()),
            number=kwargs.get('number', fake.building_number()),
            city=kwargs.get('city', fake.city()),
            state=kwargs.get('state', fake.state()),
            country=kwargs.get('country', fake.country()),
            instructions=kwargs.get('instructions', fake.text())
        )
        db_session.add(address)
        db_session.commit()
        return address
    return _address_factory