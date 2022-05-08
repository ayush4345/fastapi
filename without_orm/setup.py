from turtle import title
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

class post(BaseModel):
    title: str
    abstract: str


app=FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/create")
def create(payload: dict=Body(...)):
    print (payload)
    return {"post is created\n,new_post":f"title{payload['title']} abstract{payload['abstract']}"}


