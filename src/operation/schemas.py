from pydantic import BaseModel
from datetime import date

class OperationCreate(BaseModel):
    category_name: int
    name: str
    date: date
    value: float
    description: str
    user_id: int

class OperationDelete(BaseModel):
    id: int
    user_id:int
    
class OperationPatch(BaseModel):
    name: str
    date: date
    description: str
    
    