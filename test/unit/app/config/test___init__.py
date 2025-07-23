import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
from app.config import init_app, db, Config, TestConfig

class TestConfigInit:

    def test_init_app_applies_default_config(self):
        app = Flask(__name__)

        assert 'SQLALCHEMY_DATABASE_URI' not in app.config
        app = init_app(app)
        assert app.config['SQLALCHEMY_DATABASE_URI'] == Config.SQLALCHEMY_DATABASE_URI
        assert db is not None