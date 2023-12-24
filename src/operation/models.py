from sqlalchemy import Column, Integer, ForeignKey, Date, Float, Text, String 
from sqlalchemy.orm import relationship
from database import Base

class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable= False)
    date = Column(Date)
    value = Column(Float)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey('categories.id'))