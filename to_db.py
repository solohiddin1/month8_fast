from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database.database import Base, DATABASE_URL, get_db
from models.models import User
from pydantic import BaseModel
import jwt
from jwt.exceptions import InvalidTokenError

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)


# openssl rand -hex [number]
SECRET_KEY = 'c9d7cdd6f90cfe844124f5ec1303d04822634433f3e27472459a919db42e6b5c'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MIN = 30

class UserIn(BaseModel):
    name:str
    surname:str
    phone:str


class Token(BaseModel):
    access_token: str
    token_type: str

app = FastAPI()


@app.post("/get_all_users/")
async def get_user(db:Session = Depends(get_db)):
    return db.query(User).all()

    
@app.post("/get_user/")
async def get_user(user_id:int,db:Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()
    


@app.post("/add_user/")
async def add_user(user:UserIn,db:Session=Depends(get_db)):
    user = User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message":f"User with name {user.name} is added!"}


@app.post("/update_user/")
async def update_user(user_id:int,user:UserIn,db:Session=Depends(get_db)):
    try:
        user_data = db.query(User).filter(User.id==user_id).first()
    except Exception as e:
        print("model not found while updating user")
        return {"error":f" error while reading from model {str(e)}"}
    if user_data is not None:
            
        user_data.name = user.name
        user_data.surname = user.surname
        user_data.phone = user.phone
        db.add(user_data)
        db.commit()
        db.refresh(user_data)
        return {"message":f"user {user_id} updated!"}
    return {"error":f"user with {user_id} not found"}


@app.post("/delete_user/")
async def delete_user(user_id:int,db:Session=Depends(get_db)):
    try:
        user = db.get(User,user_id)
    except Exception as e:
        print("model not found while updating user")
        return {"error":f" error while reading from model {str(e)}"}
    print(user)
    if user is not None:
        db.delete(user)
        db.commit()
        return {"message":f"user {user_id} is deleted!"}
    return {"error":f"user with {user_id} not found"}
    