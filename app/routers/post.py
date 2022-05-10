from fastapi import APIRouter, FastAPI,status,Response,HTTPException,Depends
from ..database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session
from .. import models,schemas
from typing import List

router = APIRouter(
    prefix="/posts",
    tags = ['post']
    )

@router.get("/",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute('''SELECT * FROM posts''')
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts



#@app.get("/sqlalchemy")
#def test_posts(db: Session = Depends(get_db)):
    #posts = db.query(models.Post).all()
    #return{"data" : posts}

@router.get("/{id}",response_model=schemas.Post)
def get(id: int, response: Response):
    
    #cursor.execute('''SELECT * FROM posts where id = %s''',str(id))
    #posts = cursor.fetchone()
    
    #a= find_post(int(id))
    #if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with id:{id} not found")
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return {"message":f"post with id:{id} not found"}
   #return posts

@router.post("/" , status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
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


@router.delete("/{id}" , status_code= status.HTTP_204_NO_CONTENT)
def delete(id):
    #cursor.execute('''DELETE FROM posts where id = %s returning *''',str(id))
    #deleted_post=cursor.fetchone()
    #conn.commit()

    #if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"post with id:{id} not found")
    
    
    #my_posts.remove(a)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post )
def update(id:int, post:schemas.PostCreate):
    #cursor.execute(""" update posts set title=%s,content = %s,published = %s where id = %s returning * """
    #,(post.title,post.content,post.published,str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit
    #if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with if:{id} not found")

    #return updated_post