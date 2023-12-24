from sqlalchemy import Column, Integer, String, Date, Float, Text
from database import Base
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    operations = relationship('Operation', back_populates='category')