from pydantic import BaseModel, field_validator
from pydantic.config import ConfigDict

from app.models import UserStatus

class UpdateStatusUserSchema(BaseModel):
    status: UserStatus

    model_config = ConfigDict(extra="forbid")