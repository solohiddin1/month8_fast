import json
from fastapi import  FastAPI
from pydantic import BaseModel
from models.models import User


app = FastAPI()




class User(BaseModel):
    name:str
    surname:str
    number:str


with open('test.json', mode='a')as j:
    # json.dump()
    pass

filename = 'test.json'



@app.post("/post_1/")
async def add_user(data:User):
    users = []
    try:
        with open(filename, mode='r') as j:
            users = json.load(j)
    except (FileNotFoundError, json.JSONDecodeError):
        print("file not found or empty")
        users = []
    
    new_id = (max(int(i.get("id",0)) for i in users)+1) if users else 0

    user = data.dict()
    user["id"] = new_id
    users.append(user)
    with open(filename, mode='w') as j:
        json.dump(users, j, indent=4)
    return {"message": "user saved"}


@app.get("/")
async def get_data():
    users = []
    try:
        with open(filename, mode='r') as j:
            users = json.load(j)
    except (FileNotFoundError, json.JSONDecodeError):
        print("file not found or empty while getting data")
        users = []    

    return {"message": users}

@app.put("/put/")
async def edit_user(id: int, data: User):
    users = []
    try:
        with open(filename, mode='r') as j:
            users = json.load(j)
    except (FileNotFoundError, json.JSONDecodeError):
        print('file not found or emtpy while updating')
        users = []
    data = data.dict()
    print(data["name"])
    updated = False
    for i in users:
        if id == i["id"]:
            i.update(data)
            updated = True
    if updated:    
        with open(filename, mode='w') as j:
            json.dump(users, j, indent=4)
    else:
        {"error": "id not found!"}   
    return {"message": "field updated"}

@app.delete("/delete/")
async def delete_data(id:int):
    users = []
    try:
        with open("test.json", mode='r')as j:
            users = json.load(j)
    except (FileNotFoundError,json.JSONDecodeError):
        print("file not found or empty while deleting")
        users = []
        return {"message":"no data found!"}
    deleted = False
    for i in users:
        if id == i['id']:
            users.remove(i)
            deleted = True
    if deleted:
        with open('test.json',mode='w')as j:
            json.dump(users,j,indent=4)
        return {"message":"user deleted successfully"}
    return {"error":"user not found"}