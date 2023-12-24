from fastapi import FastAPI
import uvicorn 
from auth import models as auth_models
from item import models as item_models
from categories import models as category_models
from categories.router import router as category_router
from auth.router import router as auth_router
from database import engine
from auth.schemas import UserCreate, UserRead

app = FastAPI()

auth_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def main():
    return "Main"

app.include_router(category_router)
app.include_router(auth_router)
if __name__=="__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8080, reload = True)