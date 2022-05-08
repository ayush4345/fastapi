
from random import randrange
from fastapi import FastAPI,status,Response,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

class post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='post'
        ,cursor_factory=RealDictCursor)
        cursor=conn.cursor
        print("database connection established")
        break
    except Exception as error:
        print("connection fail")
        print("Error:",error)
        time.sleep(3)

my_posts=[{"title":"hello","content":"about title","id":1}]

app=FastAPI()

@app.get("/posts")
async def root():
    return {"data": my_posts}

def find_post(id):
    for p in my_posts:
        if (p["id"]== id):
            return p


@app.get("/posts/{id}" )
def get(id: int, response: Response):
    a= find_post(int(id))
    if not a:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with id:{id} not found")
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return {"message":f"post with id:{id} not found"}
    return{"data":a}

@app.post("/posts" , status_code=status.HTTP_201_CREATED)
def create(post: post):
    post_dict=post.dict()
    post_dict['id'] = randrange(0,1000000)
    print (post)
    my_posts.append(post_dict)
    return {"data": my_posts}


@app.delete("/posts/{id}" , status_code= status.HTTP_204_NO_CONTENT)
def delete(id):
    a=find_post(int(id))
    if not a:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"post with id:{id} not found")
    
    
    my_posts.remove(a)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
