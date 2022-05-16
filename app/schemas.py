import email
from multiprocessing.dummy import Pool
from typing import Optional
from pydantic import BaseModel,EmailStr, conint
from datetime import datetime

from sqlalchemy import Integer

class UserOut(BaseModel):
    email : EmailStr
    id : int
    created_at: datetime
    
    class Config:
        orm_mode = True



class PostBase(BaseModel):
    
    title: str
    content: str
    published: bool = True
    
    

class PostCreate(PostBase):
    pass

class Post(PostBase):
    created_at: datetime
    user_id : int
    id : int
    owner : UserOut
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str
    

    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)





