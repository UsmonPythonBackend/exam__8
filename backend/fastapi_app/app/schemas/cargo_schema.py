from typing import Optional
from pydantic import BaseModel


class CargoCreateSchema(BaseModel):
    order_id: Optional[str]
    delivery_address: Optional[str]
    delivery_status: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "order_id": "str",
            "delivery_status": "pn",
            "delivery_address": "str"
        }


class CargoUpdateSchema(BaseModel):
    order_id: Optional[str]
    delivery_address: Optional[str]
    delivery_status: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "order_id": "str",
            "delivery_status": "pn",
            "delivery_address": "str"
        }
