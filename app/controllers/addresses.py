from sqlalchemy.exc import SQLAlchemyError
from typing import Any, Optional, Dict, Union
from uuid import uuid4

from ..exceptions import DatabaseException
from ..models import db, Address, User
from .users import UserController

class AddressController:

    @staticmethod
    def get_user_address(key: str, value: str) -> Optional[Dict[str, Union[str, None]]]:
        try:
            user = db.session.execute(
                db.select(User).filter_by(**{key: value})
            ).scalar_one_or_none()

            addresses = db.session.execute(
                db.select(Address)
                .join(User, Address.user_uuid == User.uuid)
                .where(Address.user_uuid == user.uuid)
            ).scalars().all()
            return {
                'metadata': {
                    'username': user.username,
                    'length': len(addresses)
                },
                'addresses': [
                    {
                        'street': addr.street,
                        'number': addr.number,
                        'city': addr.city,
                        'state': addr.state,
                        'country': addr.country,
                        'instructions': addr.instructions
                    } for addr in addresses
                ]
            }

        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseException(original_error=str(e))
        
    @staticmethod
    def create_address(key: str, value: str, address_data: Dict[str, Any]) -> Optional[Dict[str, Union[str, None]]]:
        try:
            user = UserController.get_user(key, value)

            uuid = str(uuid4())
            new_address = Address(
                uuid = uuid,
                user_uuid = user['uuid'],
                street = address_data['street'],
                number = address_data['number'],
                city = address_data['city'],
                state = address_data['state'],
                country = address_data['country'],
                instructions = address_data['instructions']
            )
            db.session.add(new_address)
            db.session.commit()
            return {
                'username': user['username'],
                'street': new_address.street,
                'number': new_address.number,
                'city': new_address.city,
                'state': new_address.state,
                'country': new_address.country,
                'instructions': new_address.instructions
            }
        
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseException(original_error=str(e))