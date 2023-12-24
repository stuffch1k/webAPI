from pydantic import BaseModel, UUID4, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    username: str
    balance: float
    password: str


class UserLogin(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    email: str
    username: str
    balance: float

class UserPatch(BaseModel):
    username: str
    password: str
    balance: float

class UserView(BaseModel):
    id: int
    username: str