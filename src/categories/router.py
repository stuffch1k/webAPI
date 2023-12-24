from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import *
from database import get_db
from .models import *
from typing import List

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

@router.get("/", response_model=List[CategoryView])
async def get_cat( db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.patch("/", response_model=UpdateCategory)
def read_user(category: UpdateCategory, session: Session = Depends(get_db)):
    cat_db = session.query(Category).filter_by(id=category.id).first()
    if cat_db is None:
        raise HTTPException(status_code=400, detail="Invalid category ID")

    setattr(cat_db, "name", category.name)
    session.add(cat_db)
    session.commit()
    session.refresh(cat_db)
    return UpdateCategory(id=cat_db.id, name= category.name)

@router.delete("/")
async def delete_category(category_name:str, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter_by(name=category_name).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return {"message":f"category {db_category.id} was deleted"}
