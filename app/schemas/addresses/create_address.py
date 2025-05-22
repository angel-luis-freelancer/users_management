from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re
from uuid import UUID

class CreateAddressSchema(BaseModel):
    street: Optional[str] = Field(None, max_length=50, description="Name of street")
    number: Optional[int] = Field(None, gt=0, description="Street number")
    city: Optional[str] = Field(None, max_length=30, description="City")
    state: Optional[str] = Field(None, max_length=30, description="Estate")
    country: Optional[str] = Field(..., max_length=30, description="Country")
    instructions: Optional[str] = Field(None, max_length=255, description="Additional Instructions")


    @field_validator('street', 'city', 'state', 'country')
    def validate_address_fields(cls, v):
        # Remove extra spaces and validate characters
        v = ' '.join(v.strip().split())
        if not re.match(r'^[\w\s\-\.\,\áéíóúÁÉÍÓÚñÑ]+$', v):
            raise ValueError("Contains invalid characters")
        return v

    @field_validator('instructions')
    def validate_instructions(cls, v):
        if v is None:
            return v
        v = v.strip()
        if len(v) > 255:
            raise ValueError("Instructions cannot exceed 255 characters")
        return v