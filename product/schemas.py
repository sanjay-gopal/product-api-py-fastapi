from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class Product(BaseModel):
    name: str
    description: str
    price: int

class Seller(BaseModel):
    username: str
    email: str
    password: str

class DisplaySeller(BaseModel):
    username: str
    email: str
    class Config:
        orm_mode = True

class DisplayProduct(BaseModel):
    name: str
    description: str
    seller: DisplaySeller
    class Config:
        orm_mode = True

class LoginModel(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None