# creating the user
from ..import models,schemas, utils
from ..import oauth2
from fastapi import FastAPI , Body , Response , status , HTTPException , Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db
 
router = APIRouter(
  prefix="/users",
  tags=["Users"]
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_users(user : schemas.UserCreate , db: Session = Depends(get_db)):
  hashed_password = utils.Hash(user.password)
  user.password = hashed_password
  new_user = models.User(**user.dict())
  db.add(new_user)
  
  db.commit()
  db.refresh(new_user)
  return new_user

@router.get("/{id}" , response_model= schemas.UserOut)
def get_user(id : str ,  db: Session = Depends(get_db) , user_id : int = Depends(oauth2.get_current_user)) : 
  user = db.query(models.User).filter(models.User.id ==id).first()

  if not user: 
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                        detail = f"User with id {id} not found")

  return user