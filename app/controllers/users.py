from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import Any, Optional, Dict, Union
from uuid import uuid4

from ..exceptions import UserNotFoundException, UserAlreadyExistsException, InvalidUserDataException, DatabaseException
from ..models import db, User

class UserController:
    @staticmethod
    def get_user(key: str, value: str) -> Optional[Dict[str, Union[str, None]]]:
        try:
            user = db.session.execute(
                db.select(User).filter_by(**{key: value})
            ).scalar_one_or_none()
            if not user:
                raise UserNotFoundException(field=key, value=value)
            
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
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseException(original_error=str(e))

    @staticmethod
    def create_user(user_data: Dict[str, Any]) -> Dict[str, Union[str, None]]:
        try:
            user = db.session.execute(
                db.select(User).filter_by(**{'email': user_data['email']})
            ).scalar_one_or_none()
            if user:
                raise UserAlreadyExistsException(field='email', value=user_data['email'])
            
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
            if 'users.username' in str(e):
                raise DatabaseException(original_error=str(e))

            raise DatabaseException(original_error=str(e))
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseException(original_error=str(e))
        
    @staticmethod
    def update_user(key: str, value: str, user_data: Dict[str, Any]) -> str:
        try:
            result = db.session.execute(
                db.select(User).filter_by(**{key: value})
            ).first()
            user = result[0] if result else None

            if not user:
                raise UserNotFoundException(field=key, value=value)
            fields_updated = []

            for field, new_value in user_data.items():
                if new_value is None:
                    continue

                current_value = getattr(user, field, None)
                if current_value != new_value:
                    setattr(user, field, new_value)
                    fields_updated.append((field, new_value))

            if not fields_updated:
                raise InvalidUserDataException(field=key, value=value)
            
            db.session.commit()
            return {
                key: value,
                "fields_updated": fields_updated
            }
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseException(original_error=str(e))
        
    @staticmethod
    def update_user_status(key: str, value: str, status_data: Dict[str, Any]) -> Dict[str, str]:
        try:
            result = db.session.execute(
                db.select(User).filter_by(**{key: value})
            ).first()

            user = result[0] if result else None
            if not user:
                raise UserNotFoundException(field=key, value=value)

            new_status = status_data.get('status')
            user.status = new_status
            db.session.commit()
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            raise DatabaseException(original_error=str(e))