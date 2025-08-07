from pydantic import BaseModel, field_validator, model_validator, StringConstraints
from pydantic.config import ConfigDict
from typing import Annotated, Optional
import unicodedata

from app.exceptions import InvalidNullValueExeption


class UpdateUserSchema(BaseModel):
    first_name: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=2,
                max_length=30,
                strip_whitespace=True,
                pattern=r'^[a-zA-Z\s]+$'
            )
        ]
    ] = None

    middle_name: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=2,
                max_length=30,
                strip_whitespace=True,
                pattern=r'^[a-zA-Z\s]+$'
            )
        ]
    ] = None

    last_name: Optional[
        Annotated[
            str,
            StringConstraints(
                min_length=2,
                max_length=30,
                strip_whitespace=True,
                pattern=r'^[a-zA-Z\s]+$'
            )
        ]
    ] = None

    phone: Optional[
        Annotated[
            str,
            StringConstraints(
                max_length=20,
                strip_whitespace=True,
                pattern=r'^[\d\s\-\+\(\)]+$'
            )
        ]
    ] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator('first_name', 'last_name', 'middle_name')
    def normalize_and_capitalize_names(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        v = unicodedata.normalize('NFKD', v)
        v = ''.join(c for c in v if not unicodedata.combining(c))
        v = ''.join(c for c in v if c.isalpha() or c.isspace())

        def capitalize_word(word: str) -> str:
            if len(word) <= 1:
                return word.upper()
            return word[0].upper() + word[1:].lower()

        return ' '.join(capitalize_word(word) for word in v.split())

    @field_validator('phone')
    def normalize_phone(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return None
        return ''.join(c for c in v if c.isdigit() or c in '+-()')

    @model_validator(mode='after')
    def at_least_one_field(cls, values):
        data = values.model_dump()
        allowed_fields = ['first_name', 'middle_name', 'last_name', 'phone']
        if all(data.get(field) is None for field in allowed_fields):
            raise InvalidNullValueExeption(allowed_fields=allowed_fields)

        return values