from pydantic import BaseModel
from datetime import date

class OperationCreate(BaseModel):
    name: str
    date: date
    value: float
    description: str
    user_id: int
    category_id: int

class OperationDelete(BaseModel):
    id: int
    user_id:int
    
    
    
    