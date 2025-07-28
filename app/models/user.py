from enum import Enum
from typing import Dict, Union
from uuid import uuid4

from . import db

class UserStatus(str, Enum):
    ACTIVE = 'active'
    PENDING = 'pending'
    SUSPENDED = 'suspended'
    DELETED = 'deleted'

class User(db.Model):
    __tablename__ = "users"
    
    uuid = db.Column(db.String(36), primary_key=True, autoincrement=False, default=uuid4)
    first_name = db.Column(db.String(30), nullable=False)
    middle_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    status = db.Column(db.String(30), nullable=False, default=UserStatus.PENDING)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    addresses = db.relationship('Address', back_populates='user', lazy='dynamic')

    def to_dict(self) -> Dict[str, Union[str, None]]:
        return {
            'uuid': self.uuid,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'username': self.username,
            'status': self.status,
            'email': self.email,
            'phone': self.phone
        }
