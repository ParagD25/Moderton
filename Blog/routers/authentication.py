from fastapi import APIRouter,HTTPException,Depends,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from Blog.database import user_collection
from Blog.hashing import Hash
from Blog import token,convertion,models

authRouter = APIRouter(
    tags=['Authentication']
)

@authRouter.post('/authorize', response_model=models.Token)
async def login(credentials: OAuth2PasswordRequestForm = Depends()):

    user = await user_collection.find_one({"email": credentials.username})
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not Hash.verify(credentials.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    user["_id"] = convertion.convert_bson_to_json(user["_id"])
    access_token = token.create_access_token(data = {"user_id" : user["_id"]})

    return {"access_token" : access_token, "token_type":"bearer"}