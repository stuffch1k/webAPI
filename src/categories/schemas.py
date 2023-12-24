from pydantic import BaseModel
from datetime import date

class CategoryCreate(BaseModel):
    name: str

class CategoryView(CategoryCreate):
    id:int

class UpdateCategory(CategoryView):
    pass