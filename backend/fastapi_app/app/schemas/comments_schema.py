from typing import Optional
from pydantic import BaseModel


class CommentCreateSchema(BaseModel):
    client_id: Optional[str]
    furniture_id: Optional[str]
    content: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "client_id": 0,
            "furniture_id": 0,
            "content": "bir nima"
        }


class CommentUpdateSchema(BaseModel):
    furniture_id: Optional[str]
    content: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "client_id": 0,
            "furniture_id": 0,
            "content": "bir nima"
        }
