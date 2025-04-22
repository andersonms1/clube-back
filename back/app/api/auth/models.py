from datetime import datetime, UTC
from typing import Optional
from pydantic import BaseModel, Field, field_serializer, EmailStr
from bson import ObjectId
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class PasswordResetModel(BaseModel):
    email: EmailStr
