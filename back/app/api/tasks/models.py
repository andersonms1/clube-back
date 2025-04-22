from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_serializer
from bson import ObjectId
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class TaskModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    titulo: str = Field(...)
    descricao: str = Field(...)
    status: str = Field(...)
    data_vencimento: datetime = Field(...)

    @field_serializer("data_vencimento")
    def serialize_dt(self, data_vencimento: datetime, _info):
        return str(data_vencimento)


class TaskUpdateModel(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[str] = None
    data_vencimento: Optional[datetime] = None

    @field_serializer("data_vencimento")
    def serialize_dt(self, data_vencimento: datetime, _info):
        return str(data_vencimento)
