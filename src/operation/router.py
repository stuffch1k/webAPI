from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import *
from database import get_db
from .models import *
from auth.models import *
from categories.models import *
from typing import List

router = APIRouter(
    prefix="/operations",
    tags=["Operations"]
)


@router.post("/")
async def create_operation(item_create:OperationCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter_by(id=item_create.user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=400, detail="Invalid userID")
    category_db = db.query(Category).filter_by(name=item_create.category_name).first()
    if category_db is None:
        raise HTTPException(status_code=400, detail="Invalid category ID")
    db_item = Operation(name = item_create.name, 
                        date = item_create.date, value=item_create.value, 
                        description = item_create.description, 
                        user_id = existing_user.id, category_id=category_db.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    setattr(existing_user, "balance", existing_user.balance - item_create.value)
    db.add(existing_user)
    db.commit()
    db.refresh(existing_user)
    return db_item


@router.get("/", response_model=List[OperationCreate])
async def read_operations(db: Session = Depends(get_db)):
    return db.query(Operation).all()

@router.get("/{category_id}",response_model= List[OperationCreate])
async def read_item(category_id: int, db: Session = Depends(get_db)):
    items = db.query(Operation).filter_by(category_id=category_id).all()
    return items

@router.get("/{user_id}",response_model= List[OperationCreate])
async def read_item(user_id: int, db: Session = Depends(get_db)):
    items = db.query(Operation).filter_by(user_id=user_id).all()
    return items

@router.patch("/{operation_id}")
async def read_item(operation_id: int, data: OperationPatch, db: Session = Depends(get_db)):
    item_db = db.query(Operation).filter_by(id=operation_id).first()
    if item_db is None:
        raise HTTPException(status_code=400, detail="Invalid Operation ID")
    for key, value in data.items():
        if hasattr(item_db, key):
            setattr(item_db, key, value)
    db.commit()
    db.refresh(item_db)
    return item_db

@router.delete("/")
async def delete_item(operation: OperationDelete, db: Session = Depends(get_db)):
    db_operation = db.query(Category).filter_by(name=operation.id).first()
    if db_operation:
        if db_operation.user_id == operation.user_id:
            db.delete(db_operation)
            db.commit()
        raise HTTPException(status_code=400, detail="Invalid userID")
    return {"message":f"category {db_operation.id} was deleted"}

