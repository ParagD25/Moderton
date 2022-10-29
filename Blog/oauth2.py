from Blog.database import user_collection
from Blog.token import verify_access_token
from fastapi import Depends,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from Blog.convertion import convert_json_to_bson

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authorize")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exceptions = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Can not verify credentials", headers={
        "WWW-Authenticate": "Bearer"
    })
    token = verify_access_token(token, credentials_exceptions)
    user = await user_collection.find_one({"_id" : convert_json_to_bson(token.id)})
    return user