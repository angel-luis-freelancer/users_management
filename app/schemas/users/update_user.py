from typing import Annotated, Optional
from pydantic import BaseModel, StringConstraints

class UserUpdateSchema(BaseModel):
    first_name: Optional[
        Annotated[
            str,
            StringConstraints(
                max_length=30,
                strip_whitespace=True
            )
        ]
    ] = None
    last_name: Optional[
        Annotated[
            str,
            StringConstraints(
                max_length=30,
                strip_whitespace=True
            )
        ]
    ] = None
    phone: Optional[
        Annotated[
            str,
            StringConstraints(
                max_length=20,
                strip_whitespace=True
            )
        ]
    ] = None