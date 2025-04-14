from app.config import db  

from .user import User
from .address import Address

__all__ = ['db', 'User', 'Address']