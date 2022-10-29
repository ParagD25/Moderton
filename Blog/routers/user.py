from fastapi import APIRouter,HTTPException,Depends,status
from typing import List
from Blog.hashing import Hash
from Blog.models import User, UserShow
from Blog.database import user_collection
from Blog import oauth2

userRouter = APIRouter(
    prefix="/user",
    tags = ["User"]
)


@userRouter.get("/",status_code=status.HTTP_200_OK,response_model=List[UserShow])
async def get_users(current_user : int = Depends(oauth2.get_current_user)):
    listout = []
    cluster = user_collection.find({})

    async for doc in cluster:
        listout.append(doc)
        
    return listout


@userRouter.post("/create",status_code=status.HTTP_201_CREATED,response_model=UserShow)
async def add_user(user: User):
    exists = await user_collection.find_one({'email': user.email})

    if exists:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email Id already exists. Try Another.")

    new_user = user.dict()
    new_user['password'] = Hash.bcrypt(new_user['password'])

    res = await user_collection.insert_one(new_user)
    return new_user