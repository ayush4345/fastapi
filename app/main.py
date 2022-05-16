from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine
from . import models
from .routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message":"hello world"}


