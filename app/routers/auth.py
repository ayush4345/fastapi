from fastapi import APIRouter, FastAPI,status,Response,HTTPException,Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from .. import models,schemas,utils,Oauth2
from .. import database

router = APIRouter(prefix ='/login', tags=['Authentication'])

@router.post('/',response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db:Session =Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = f"invalid credentials")

    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,detail = f"invalid credentials"
        )
    access_token = Oauth2.create_access_token(data = {"user_id" : user.id})

    
    return {"access_token": access_token,"token_type":"bearer"}


