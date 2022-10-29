from datetime import timedelta, datetime
from jose import JWTError,jwt
from Blog.models import TokenData


SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    ret = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return ret


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if not id:
            raise credentials_exception
        token_data = TokenData(id=id)
        
    except JWTError:
        raise credentials_exception

    return token_data