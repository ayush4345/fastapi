from random import randrange
from fastapi import FastAPI,status,Response,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

class post(BaseModel):
    id:int
    title: str
    content: str
    published: bool = True

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

my_posts=[{"title":"hello","content":"about title","id":1}]

app=FastAPI()

@app.get("/posts")
def root():
    cursor.execute('''SELECT * FROM posts''')
    posts = cursor.fetchall()
    return {"data": posts}

def find_post(id):
    for p in my_posts:
        if (p["id"]== id):
            return p


@app.get("/posts/{id}" )
def get(id: int, response: Response):
    
    cursor.execute('''SELECT * FROM posts where id = %s''',str(id))
    posts = cursor.fetchone()
    
    #a= find_post(int(id))
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with id:{id} not found")
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return {"message":f"post with id:{id} not found"}
    return{"data":posts}

@app.post("/posts" , status_code=status.HTTP_201_CREATED)
def create(post: post):
    cursor.execute('''insert into posts (id,title,content,published) values(%s,%s,%s,%s) returning * ''',(post.id,post.title
    ,post.content,post.published))
   
    new_posts=cursor.fetchone()
    conn.commit()
    
    
    return {"data": new_posts}


@app.delete("/posts/{id}" , status_code= status.HTTP_204_NO_CONTENT)
def delete(id):
    cursor.execute('''DELETE FROM posts where id = %s returning *''',str(id))
    deleted_post=cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"post with id:{id} not found")
    
    
    #my_posts.remove(a)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}" )
def update(id:int, post:post):
    cursor.execute(""" update posts set title=%s,content = %s,published = %s where id = %s returning * """
    ,(post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with if:{id} not found")

    return{"data":updated_post}