from typing import Any, Optional, Dict, Union
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from uuid import uuid4

from ..models import db, Address

class UserController:

    @staticmethod
    def get_address():
        pass