from ..import models , schemas , oauth2
from fastapi import FastAPI , Body , Response , status , HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import func
from ..database import  get_db
from typing import Optional
from typing import List , Any , cast
router = APIRouter(
  prefix="/posts", 
  tags = ["Post"]
)                                                       

# getting all the posts

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db) , current_user  = Depends(oauth2.get_current_user) 
              , limit : int  = 10 , skip : int = 0 , search : Optional[str] = ""):
  # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  print(posts)

  return posts

# so with post request we can end data while with get we only get data not posting data 

my_posts = [{"title": 'title of post 1' , "content" : "content of post 1", "id" : 1} , {"title" : "Fvaourite foods" , "content": ' i like pizza' , "id" : 2}]
def find_post(id) : 
  for p in my_posts : 
    if p["id"] == id :
      return p


# getting the latest post
@router.get("/latest")
def get_latest_post():
  latest_post = my_posts[len(my_posts) - 1]
  return {"detials" : latest_post}



# creating the post 

@router.post("/", status_code = status.HTTP_201_CREATED ,response_model = schemas.Post )
def create_posts( post : schemas.PostCreate , db: Session = Depends(get_db) , current_user  = Depends(oauth2.get_current_user)):
  new_post = models.Post(owner_id=current_user.id ,**post.dict())

  db.add(new_post)
  db.commit()
  print(current_user)
  db.refresh(new_post)
  return new_post
  

# cursor.execute("""INSERT INTO posts (title , content , published) values(%s,%s,%s)
#   RETURNING * """
#                ,(post.title , post.content , post.published))
# new_post = cursor.fetchone()
# conn.commit()
  
# getting the post with specific id 

@router.get("/{id}", response_model = schemas.PostOut)  # this {id} is the path parameter
def get_the_post(id : int , response : Response , db : Session = Depends(get_db) ,current_user  = Depends(oauth2.get_current_user)):
  # cursor.execute("""SELECT  * FROM posts where id  = %s""" , (str(id)))
  # post =cursor.fetchone()
  post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
  print(post)
  if not post : 
    raise HTTPException(status.HTTP_404_NOT_FOUND, 
                        detail = f"Post wth id {id} was not found")
  return post 

# deleting the specific post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int , db : Session = Depends(get_db) , current_user   = Depends(oauth2.get_current_user)):
  # cursor.execute(""" DELETE FROM posts where id = %s returning * """, (str(id) , ))
  # deleted_post = cursor.fetchone()
  # conn.commit()
  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()
  if post is None :
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f"Post with id {id} does not exists")
  if post.owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail = f"Not authorize3d to perform requested action")

  
  post_query.delete(synchronize_session=False)
  db.commit()
  return Response(status_code = status.HTTP_204_NO_CONTENT)

#updating the specific post 

@router.put("/{id}",response_model= schemas.Post)
def update_post(id: int, updating_post: schemas.PostUpdate, db: Session = Depends(get_db) , current_user  = Depends(oauth2.get_current_user) ):
  post_query = db.query(models.Post).filter(models.Post.id == id)
  existing_post = post_query.first()
  if existing_post is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Post with id {id} does not exist",
    )

  if existing_post.owner_id != current_user.id :
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail = f"Not authorized to perform requested action")
  

  post_query.update(cast(dict[Any, Any], updating_post.model_dump()), synchronize_session=False)
  db.commit()

  return post_query.first()