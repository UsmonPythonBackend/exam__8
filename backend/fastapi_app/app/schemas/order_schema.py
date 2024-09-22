from typing import Optional
from pydantic import BaseModel


class OrderCreateSchema(BaseModel):
    order_status: Optional[str]
    furniture_id: Optional[str]
    quantity: Optional[int]
    total_price: Optional[float]

    class Config:
        orm_mode = True
        schema_extra = {
            "order_status": "pn",
            "furniture_id": "str",
            "quantity": 50,
            "total_price": 23.1
        }


class OrderUpdateSchema(BaseModel):
    order_status: Optional[str]
    furniture_id: Optional[str]
    quantity: Optional[int]
    total_price: Optional[float]

    class Config:
        orm_mode = True
        schema_extra = {
            "order_status": "pn",
            "furniture_id": "str",
            "quantity": 50,
            "total_price": 23.1
        }
