from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import *
from database import get_db 
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from .models import User
import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from .utils import *

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"]
)

@router.post("/register")
def create_user(user: UserCreate, session: Session = Depends(get_db)):
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
    return {"message":"user created successfully", "user_id":user_data.id, "username": user_data.username}


@router.post("/user_info", response_model=UserRead)
def read_user(user: UserLogin, session: Session = Depends(get_db)):
    existing_user = session.query(User).filter_by(email=user.username).first()
    if existing_user is None:
        raise HTTPException(status_code=400, detail="Invalid username")
    hashed_pass = existing_user.hashed_password
    if not verify_password(user.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    return UserRead(id=existing_user.id, email = existing_user.email, username= existing_user.username, balance=existing_user.balance)

@router.patch("/user_patch", response_model=UserRead)
def read_user(user: UserPatch, session: Session = Depends(get_db)):
    existing_user = session.query(User).filter_by(email=user.username).first()
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
    return UserRead(id=existing_user.id, email = existing_user.email, username= existing_user.username, balance=existing_user.balance)



  
# @router.post('/login')
# def login(user_schema: UserLogin, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == user_schema.username).first()
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
#     hashed_pass = user.password_hash
#     if not verify_password(user_schema.password, hashed_pass):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect password"
#         )
    
#     access=create_access_token(user.id)
#     refresh = create_refresh_token(user.id)

#     token_db = TokenTable(user_id=user.id,  access_toke=access,  refresh_toke=refresh, status=True)
#     db.add(token_db)
#     db.commit()
#     db.refresh(token_db)
#     return {
#         "access_token": access,
#         "refresh_token": refresh,
#     }

# @router.get('/getusers')
# def getusers( dependencies=Depends(JWTBearer()),session: Session = Depends(get_db)):
#     user = session.query(User).all()
#     return user