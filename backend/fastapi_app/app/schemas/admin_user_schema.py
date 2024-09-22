from pydantic import BaseModel, EmailStr, Field, constr, validator
from typing import Optional
from pydantic import BaseModel, validator, constr
import re


class Settings(BaseModel):
    authjwt_secret_key: str = "6a02f43b64443808e2ad95a45e8ae3da90495937a533ed13e268d39cf907a3fb"


class UserRegisterSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[str]
    phone: constr(regex=r'^\+?\d{9,15}$')
    password: constr(min_length=8)

    @validator('password')
    def validate_password(cls, value):
        if not re.search(r"[A-Za-z]", value) or not re.search(r"\d", value):
            raise ValueError("Password must contain both letters and numbers.")
        return value

    @validator('first_name', 'last_name')
    def strip_names(cls, value):
        return value.strip()

    class Config:
        orm_mode = True
        schema_extra = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "password": "Password123"
        }


class UserLoginSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "username": "johndoe",
            "password": "Password123"
        }


class PasswordResetSchema(BaseModel):
    password: Optional[str]
    password_2: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "password": "Password123",
            "password_2": "Password123"
        }
