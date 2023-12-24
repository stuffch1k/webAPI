from pydantic import BaseModel
from datetime import date

class OperationCreate(BaseModel):
    category_name: str
    name: str
    date: date
    value: float
    description: str
    user_id: int

class OperationDelete(BaseModel):
    id: int
    user_id:int
    
class OperationPatch(BaseModel):
    date: date
    description: str
    
class OperationView(OperationPatch):
    id:int
    value:float
    user_id:int
    category_id:int    
