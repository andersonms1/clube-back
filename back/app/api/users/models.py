from datetime import datetime, UTC
from typing import Optional
from pydantic import BaseModel, Field, field_serializer, EmailStr
from bson import ObjectId
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: EmailStr
    username: str
    password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_serializer("created_at")
    def serialize_dt(self, created_at: datetime, _info):
        return str(created_at)

    @field_serializer("updated_at")
    def serialize_dt(self, updated_at: datetime, _info):
        return str(updated_at)


class UserResponse(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: EmailStr
    username: str
    created_at: Optional[datetime]

    @field_serializer("created_at")
    def serialize_dt(self, created_at: datetime, _info):
        return str(created_at)
