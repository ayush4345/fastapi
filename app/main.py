import email
from random import randrange
from fastapi import FastAPI,status,Response,HTTPException,Depends
from fastapi.params import Body

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas,util
from .database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session
from .routers import post,user




models.Base.metadata.create_all(bind=engine)

app=FastAPI()





while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='post'
        ,cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("database connection established")
        break
    except Exception as error:
        print("connection fail")
        print("Error:",error)
        time.sleep(3)



app.include_router(post.router)
app.include_router(user.router)



