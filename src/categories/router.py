from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import *
from database import get_db
from .models import *

router = APIRouter(
    prefix="/category",
    tags=["Category"]
)


@router.post("/")
async def create_category(category_schema:CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(**category_schema.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/")
async def get_cat(name:str, db: Session = Depends(get_db)):
    user = db.query(Category).filter_by(name=name).first()
    return user
