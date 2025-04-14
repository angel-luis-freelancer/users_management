import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import TestConfig
from app.models import db 
from app.config.settings import TestConfig

@pytest.fixture(scope='session')
def db_engine():
    """Crea un motor SQLite en memoria para testing"""
    engine = create_engine(TestConfig.SQLALCHEMY_DATABASE_URI)
    db.metadata.create_all(engine)
    yield engine
    db.metadata.drop_all(engine)
    engine.dispose()

@pytest.fixture
def db_session(db_engine):
    """Provee una sesión de base de datos para cada test"""
    connection = db_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=db_engine)
    session = Session()
    db.session = session
    yield session
    session.close()
    transaction.rollback()
    connection.close()