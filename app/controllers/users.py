from typing import Any, Optional, Dict, Union
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from uuid import uuid4

from ..models import db, User

class UserController:
    @staticmethod
    def get_user(key: str, value: str) -> Optional[Dict[str, Union[str, None]]]:
        try:
            user = db.session.execute(
                db.select(User).filter_by(**{key: value})
            ).scalar_one_or_none()
        
            if user:
                return {
                    'uuid': user.uuid,
                    'first_name': user.first_name,
                    'middle_name': user.middle_name,
                    'last_name': user.last_name,
                    'username': user.username,
                    'status': user.status,
                    'email': user.email,
                    'phone': user.phone
                }
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Error getting user: {str(e)}")

    @staticmethod
    def create_user(user_data: Dict[str, Any]) -> Dict[str, Union[str, None]]:
        try:
            uuid = str(uuid4())

            new_user = User(
                uuid=uuid,
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                username=f"{user_data['first_name']}{user_data['last_name']}".lower(),
                email=user_data['email'],
                phone=user_data.get('phone'),  # Opcional
                middle_name=user_data.get('middle_name'),  # Opcional
                status='active'  # default value
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user.to_dict()

        except IntegrityError as e:
            db.session.rollback()
            if 'username' in str(e):
                raise ValueError("The username already exists")
            elif 'email' in str(e):
                raise ValueError("The email already exists")
            raise ValueError("Database integrity error")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Error creating the user: {str(e)}")