from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
from .routers import post , user , auth , vote 
from .import models 
from .database import engine 
from .config import Settings

# models.Base.metadata.create_all(bind = engine) 

# this is what creates the table what it does is just go and 
# and search for the table name and if it finds any table exisiting with that name it simply would not creat any other table
# so it cannot modify anything this way 
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
  return {"message" : "Welcome to my api endpoint "}
