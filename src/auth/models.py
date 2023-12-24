from sqlalchemy import Column, Integer, Float, Text, String, Boolean, DateTime
from database import Base
from datetime import datetime

class User( Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    balance = Column(Float, default=0)
    email = Column(Text, unique=True)
    username = Column(Text, unique=True)
    hashed_password = Column(Text)
