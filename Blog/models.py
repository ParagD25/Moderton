from pydantic import BaseModel,EmailStr,Field
from typing import Optional
from bson import ObjectId
import datetime

class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Blog(BaseModel):
    title:str
    content:str

class BlogShow(Blog):
    id: Optional[PyObjectId]=Field(alias='_id')
    user: Optional[str]=None
    blog_created: datetime.datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        } 

class User(BaseModel):
    email: EmailStr
    password: str

class UserShow(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    
    class Config:
        json_encoders = {ObjectId: str}
        orm_mode = True


class Token(BaseModel):
    access_token: str 
    token_type: str 

class TokenData(BaseModel):
    id: Optional[str] = None
    