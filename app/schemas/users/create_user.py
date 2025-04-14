from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, field_validator, StringConstraints
import unicodedata

class UserCreateSchema(BaseModel):
    first_name: Annotated[
        str,
        StringConstraints(
            min_length=1,
            max_length=30,
            strip_whitespace=True,
            pattern=r'^[a-zA-Z\s]+$'
        )
    ]
    last_name: Annotated[
        str,
        StringConstraints(
            min_length=1,
            max_length=30,
            strip_whitespace=True,
            pattern=r'^[a-zA-Z\s]+$'
        )
    ]
    email: EmailStr
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

    @field_validator('first_name', 'last_name')
    def normalize_and_capitalize_names(cls, v: str) -> str:
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

    @field_validator('email')
    def normalize_email(cls, v: str) -> str:
        return v.lower().strip()

    @field_validator('phone')
    def normalize_phone(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return None
        return ''.join(c for c in v if c.isdigit() or c in '+-() ').strip()