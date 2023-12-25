from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import *
from database import get_db 
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from .models import User
import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import List, Any
from .utils import *
from chat.utils import notify_observers

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post("/register")
async def create_user(user: UserCreate, session: Session = Depends(get_db)):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_user = session.query(User).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    encrypted_password = get_hashed_password(user.password)

    new_user = User(username=user.username, email=user.email, hashed_password=encrypted_password, balance = user.balance )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    user_data = session.query(User).filter_by(email=user.email).first()
    await notify_observers(f"User {user.username} registered at this service")
    return {"message":"user created successfully", "user_id":user_data.id, "username": user_data.username}


@router.post("/user_info", response_model=UserRead)
def read_user(user: UserLogin, session: Session = Depends(get_db)):
    existing_user = session.query(User).filter_by(username=user.username).first()
    if existing_user is None:
        raise HTTPException(status_code=400, detail="Invalid username")
    hashed_pass = existing_user.hashed_password
    if not verify_password(user.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    return UserRead(id=existing_user.id, email = existing_user.email, username= existing_user.username, balance=existing_user.balance)

@router.get("/", response_model=List[UserView])
async def read_users(session: Session = Depends(get_db)):
    return session.query(User.id, User.username).all()

@router.patch("/user_patch", response_model=UserRead)
async def read_user(user: UserPatch, session: Session = Depends(get_db)):
    existing_user = session.query(User).filter_by(username=user.username).first()
    if existing_user is None:
        raise HTTPException(status_code=400, detail="Invalid username")
    hashed_pass = existing_user.hashed_password
    if not verify_password(user.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    setattr(existing_user, "balance", user.balance)
    session.add(existing_user)
    session.commit()
    session.refresh(existing_user)
    await notify_observers(f"The balance of user {existing_user.username} was changed")
    return UserRead(id=existing_user.id, email = existing_user.email, username= existing_user.username, balance=existing_user.balance)

@router.delete("/")
async def read_users(user:UserLogin, session: Session = Depends(get_db)):
    existing_user = session.query(User).filter_by(username=user.username).first()
    if existing_user is None:
        raise HTTPException(status_code=400, detail="Invalid username")
    hashed_pass = existing_user.hashed_password
    if not verify_password(user.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    session.delete(existing_user)
    session.commit()
    await notify_observers(f"User {user.username} deleted his profile")
    return {"message":f"User {user.username} was deleted"}