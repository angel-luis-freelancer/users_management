from typing import Dict, Union
from . import db

class Address(db.Model):
    __tablename__ = "addresses"
    
    uuid = db.Column(db.String(36), primary_key=True)
    user_uuid = db.Column(db.String(36), db.ForeignKey('users.uuid'))
    street = db.Column(db.String(50))
    number = db.Column(db.Integer)
    city = db.Column(db.String(30))
    state = db.Column(db.String(30))
    country = db.Column(db.String(30))
    instructions = db.Column(db.String(255))
    user = db.relationship('User', back_populates='addresses')

    def to_dict(self) -> Dict[str, Union[str, None]]:
        return {
            'uuid': self.uuid,
            'user_uuid': self.user_uuid,
            'street': self.street,
            'number': self.number,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'instructions': self.instructions
        }