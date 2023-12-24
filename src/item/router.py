from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import *
from database import get_db

router = APIRouter(
    prefix="/operations",
    tags=["Operations"]
)


@router.post("/")
async def create_operation(item_create:ItemCreate, db: Session = Depends(get_db)):
    pass
