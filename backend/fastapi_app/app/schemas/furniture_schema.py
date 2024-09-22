from typing import Optional
from pydantic import BaseModel


class FurnitureCreateSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]
    quantity: Optional[int]
    image_url: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "chair",
            "description": "this is a chair",
            "price": 45,
            "quantity": 50,
            "image_url": "https://cdn0.divan.by/img/v1/p6zGYcUmfU4jylci300Lssq1qRvBkRd2qksF6wCllRQ/t:0::0:0/pd:60:60:60:60/rs:fit:1148:720:0:1:ce:0:0/g:ce:0:0/bg:f5f3f1/q:85/czM6Ly9kaXZhbi9wcm9kdWN0LzUwOTY4NDMucG5n.jpg"
        }


class FurnitureUpdateSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]
    quantity: Optional[int]
    image_url: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "chair",
            "description": "this is a chair",
            "price": 45,
            "quantity": 50,
            "image_url": "https://cdn0.divan.by/img/v1/p6zGYcUmfU4jylci300Lssq1qRvBkRd2qksF6wCllRQ/t:0::0:0/pd:60:60:60:60/rs:fit:1148:720:0:1:ce:0:0/g:ce:0:0/bg:f5f3f1/q:85/czM6Ly9kaXZhbi9wcm9kdWN0LzUwOTY4NDMucG5n.jpg"
        }
