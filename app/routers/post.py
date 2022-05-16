from fastapi import APIRouter, FastAPI,status,Response,HTTPException,Depends
from sqlalchemy import func
from ..database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session
from .. import models,schemas,Oauth2
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags = ['post']
    )

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user :int = 
Depends(Oauth2.get_current_user),limit: int = 10,skip :int = 0,search : Optional[str] = ""):
    
    #for getting post specific to user that is login
    #posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,
    isouter = True).group_by(models.Post.id).all()
    return results



 
@router.get("/{id}",response_model=schemas.Post)
def get(id: int, db: Session = Depends(get_db),current_user :int = 
Depends(Oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with id:{id} not found")
        
    return post

@router.post("/" , status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create(post: schemas.PostCreate,db: Session = Depends(get_db),current_user :int = 
Depends(Oauth2.get_current_user)):
   
    print(current_user.email)
    new_posts = models.Post(user_id = current_user.id,**post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    
    return new_posts


@router.delete("/{id}" , status_code= status.HTTP_204_NO_CONTENT,)
def delete(id: int,db: Session = Depends(get_db),current_user :int = 
Depends(Oauth2.get_current_user)):
    #cursor.execute('''DELETE FROM posts where id = %s returning *''',str(id))
    #deleted_post=cursor.fetchone()
    #conn.commit()
    post_query= db.query (models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"post with id:{id} not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"Not authorized for performing this post")

    post_query.delete(synchronize_session= False)
    db.commit()
    

@router.put("/{id}",response_model=schemas.Post )
def update(id:int,updated_post:schemas.PostCreate,db: Session = Depends(get_db),current_user :int = 
Depends(Oauth2.get_current_user)):
    
    post_query= db.query (models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with if:{id} not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"Not authorized for performing this post")

    post_query.update(updated_post.dict(),synchronize_session=False)

    db.commit()

    return post_query.first()
