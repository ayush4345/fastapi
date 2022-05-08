from psycopg2 import Date
from pydantic import BaseModel,EmailStr
from datetime import datetime

class PostBase(BaseModel):
    
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    created_at: datetime
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email : EmailStr
    password : str
    
class UserOut(BaseModel):
    email : EmailStr
    id : int
    created_at: datetime
    class Config:
        orm_mode = True
    





