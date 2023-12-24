from pydantic import BaseModel
from datetime import date

class ItemCreate(BaseModel):
    
    name: str
    category_name: str
    value: float
    description: str
    date: date