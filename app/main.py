# from fastapi import FastAPI,HTTPException
# from pydantic import BaseModel
# from typing import Optional
# from math import dist
# import psycopg2
# from psycopg2.extras import RealDictCursor
# from sqlalchemy.orm import Session
# from . import models, schemas, crud
# from .database import engine, Base, get_db

# app=FastAPI()


# Base.metadata.create_all(bind=engine)

# try :
#     conn = psycopg2.connect(
#         host="localhost",
#         database="fastapidatabase",
#         user="postgres",
#         password="sourabh@2175",
#         cursor_factory=psycopg2.extras.RealDictCursor
#         )
#     cursor=conn.cursor()
#     print("Database connection successful")
# except psycopg2.Error as e:
#         print(f"Error: {e}")


# class user(BaseModel):
#     name: str
#     price: str
#     # id: bool = True
#     # rating: Optional[int] = None
#     # description: Optional[str] = None

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}



# # @app.post("/posts")
# # def create_post(post: Post):
# #     print(post.dict()) 

# #     # cursor.execute(""" SELECT * FROM users; """)
# #     # posts=cursor.fetchall()

# #     cursor.execute(""" INSERT INTO users (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
# #     posts=cursor.fetchone()
# #     conn.commit()
# #     # print(post)
# #     return {"message": f"post created{posts}"}

# # This is read operation
# @app.get("/posts")
# def read_posts():
     
#      cursor.execute(""" SELECT * FROM users """)
#      posts=cursor.fetchall()

#      if not posts:
#             raise HTTPException(status_code=404, detail=f"posts was not found")

#      return {"data": posts}

# #write operation

# @app.post("/addpost")
# def get_post(user:user):
#      cursor.execute("""INSERT INTO users (name,price) VALUES (%s,%s) RETURNING * """, (user.name,user.price))
#      new_post=cursor.fetchone()
#      conn.commit()

#      if not new_post:
#             raise HTTPException(status_code=404, detail=f"posts was not created")

#      return {"data": new_post}


# # getting a single product

# @app.get("/posts/{id}")
# def get_post(id:int):
#       cursor.execute(""" SELECT * FROM users WHERE id = %s """, (str(id),))
#       post=cursor.fetchone()
#       if not post:
#             raise HTTPException(status_code=404, detail=f"post with id {id} was not found")
      
#       return {"data": post}

# #delecting data from database

# @app.delete("/posts/{id}")
# def delete_post(id:int):
#       cursor.execute("DELETE FROM users WHERE id = %s RETURNING *", (str(id),))
#       deleted_post=cursor.fetchone()
#       conn.commit()

#       if not deleted_post:
#             raise HTTPException(status_code=404, detail=f"post with id {id} was not found")

#       return {"data": deleted_post}


# #update from database

# @app.put("/posts/{id}")
# def update_post(id:int,user:user):
#       cursor.execute(""" UPDATE users SET name = %s , price = %s WHERE id = %s RETURNING * """, (user.name,user.price,str(id)))
#       updated_post=cursor.fetchone()
#       conn.commit()

#       if not updated_post:
#             raise HTTPException(status_code=404, detail=f"post with id {id} was not found")

#       return {"data": updated_post}



# main.py
from typing import Optional, List
from . import models
from . import crud
from passlib.context import CryptContext
from fastapi import FastAPI, Depends, HTTPException,status
from sqlalchemy.orm import Session
from . import schemas
from .database import engine, Base, get_db
from passlib.context import CryptContext
from .  import oauth
#jwt import below
from fastapi.security import OAuth2PasswordRequestForm


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize the database
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()


#post apis below

#get all post api
@app.get("/posts", response_model=List[schemas.PostSchema])
def read_posts(db: Session = Depends(get_db),):
    return crud.get_posts(db)

#create the post for a user 
@app.post("/posts")
def create_post(post: schemas.PostSchema, db: Session = Depends(get_db), current_user:int = Depends(oauth.get_current_user)):
    return crud.create_post(db, post, current_user)

#api for deleting post 
@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user:int = Depends(oauth.get_current_user)):
    return crud.delete_post(db, id, current_user)

#api for updating post
@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostSchema, db: Session = Depends(get_db), current_user:int = Depends(oauth.get_current_user)):
    return crud.update_post(db, id, post, current_user)

#get post of sepecific user
@app.get("/users/{id}/posts")
def get_user_posts(id: int, db: Session = Depends(get_db)):
    return crud.get_user_posts(db, id)













#creating users 
@app.post("/createuser",status_code=status.HTTP_201_CREATED,response_model=schemas.Respone)
def create_user(user:schemas.UserSchema,db:Session=Depends(get_db)):
    return crud.create_user(db,user)

# getting a single user by id
@app.get("/users/{id}",status_code=status.HTTP_200_OK)
def get_user(id:int,db:Session=Depends(get_db)):
    return crud.get_user(db,id)


#login user
# def login_user(user:schemas.LoginSchema,db:Session=Depends(get_db)):
@app.post("/login",status_code=status.HTTP_200_OK)
def login_user(user:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
     #OAuth2PasswordRequestForm  it have only two fields username and password
     #check if user exists
     userdb=db.query(models.User).filter(models.User.email == user.username).first()
     if not userdb:
          raise HTTPException(status_code=404, detail="User not found")
     #check if password is correct
     print(userdb)
     if not pwd_context.verify(user.password,userdb.password):
          raise HTTPException(status_code=404, detail="user credentials are not correct")
     
     print(type(userdb.id))
     #create token
     access_token=oauth.create_access_token(data={"user_id":userdb.id})
     
     return {"access_token":access_token,"token_type":"bearer",}


# Now we are create first protected route which will give us all users just for testing jwt
@app.get("/users",status_code=status.HTTP_200_OK)
def get_all_users(db:Session=Depends(get_db), current_user:int=Depends(oauth.get_current_user)):
    print("current user",current_user.id)    
    posts=db.query(models.User).all()
    if not posts:
        raise HTTPException(status_code=404, detail=f"posts was not found")

    return {"data": posts}


#vote api

@app.post("/vote",status_code=status.HTTP_200_OK)
def vote(vote:schemas.VoteSchema,db:Session=Depends(get_db),current_user:int=Depends(oauth.get_current_user)):
    return crud.create_vote(db,vote,current_user)