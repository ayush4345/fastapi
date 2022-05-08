import email
from random import randrange
from fastapi import FastAPI,status,Response,HTTPException,Depends
from fastapi.params import Body
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas,util
from .database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session




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




@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute('''SELECT * FROM posts''')
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts



#@app.get("/sqlalchemy")
#def test_posts(db: Session = Depends(get_db)):
    #posts = db.query(models.Post).all()
    #return{"data" : posts}

@app.get("/posts/{id}",response_model=schemas.Post)
def get(id: int, response: Response):
    
    cursor.execute('''SELECT * FROM posts where id = %s''',str(id))
    posts = cursor.fetchone()
    
    #a= find_post(int(id))
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with id:{id} not found")
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return {"message":f"post with id:{id} not found"}
    return posts

@app.post("/posts" , status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create(post: schemas.PostCreate,db: Session = Depends(get_db)):
    #cursor.execute('''insert into posts (id,title,content,published) values(%s,%s,%s,%s) returning * ''',(post.id,post.title
    #,post.content,post.published))
   
    #new_posts=cursor.fetchone()
    #conn.commit()
    new_posts = models.Post(title=post.title,content= post.content,published = post.published)
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    
    return new_posts


@app.delete("/posts/{id}" , status_code= status.HTTP_204_NO_CONTENT)
def delete(id):
    cursor.execute('''DELETE FROM posts where id = %s returning *''',str(id))
    deleted_post=cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"post with id:{id} not found")
    
    
    #my_posts.remove(a)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",response_model=schemas.Post )
def update(id:int, post:schemas.PostCreate):
    cursor.execute(""" update posts set title=%s,content = %s,published = %s where id = %s returning * """
    ,(post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with if:{id} not found")

    return updated_post


@app.post("/users" , status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user : schemas.UserCreate,db: Session = Depends(get_db)):
    
    #has the password = user.password
    
    hashed_password=util.hash(user.password)
    user.password = hashed_password

    new_user= models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

