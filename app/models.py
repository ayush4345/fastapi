import string
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import TIMESTAMP, Column,Integer,String,Boolean,Text

class Post(Base):
    __tablename__="posts"

    id=Column(Integer,primary_key=True,nullable=False)
    title = Column (String,nullable=False)
    content=Column(String,nullable=False)
    published =Column(Boolean,server_default='True')
    created_at =Column(TIMESTAMP(timezone=True),nullable = False,server_default=text('now()'))


class User(Base):
    __tablename__="users"
    email = Column(String,nullable = False,unique = True)
    id = Column(Integer,primary_key =True,nullable = False)
    password = Column (String,nullable = False)
    created_at =Column(TIMESTAMP(timezone=True),nullable = False,server_default=text('now()'))