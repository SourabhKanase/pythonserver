# crud.py
from . import models
from sqlalchemy.orm import Session
from . import schemas
from passlib.context import CryptContext
from .database import engine
from fastapi import HTTPException
from fastapi import Depends
from . import oauth
#jwt import below


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)


#post apis below

#get all post api
def get_posts(db: Session):
    return db.query(models.Post).all()

#deleting the post
def delete_post(db, id, current_user):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}

#updating the post
def update_post(db, id, post, current_user):
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not updated_post:
        raise HTTPException(status_code=404, detail=f"post with id {id} was not found")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    updated_post.title = post.title
    updated_post.content = post.content
    updated_post.published = post.published
    db.commit()
    return {"data": updated_post}

#getting post of sepecific user
def get_user_posts(db: Session, id: int):
    return db.query(models.Post).filter(models.Post.owner_id == id).all()

def create_post(db: Session, post: schemas.PostSchema, current_user):
    print("current user",current_user.id)
    # print(current_user.id)
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    # new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def create_user(db: Session, user: schemas.UserSchema):
     # Check if the email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    # print(user)
    # print(user.dict())
    hased_password = pwd_context.hash(user.password)
    user.password = hased_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db: Session, id: int):
    user= db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def create_vote(db, vote, current_user):

   # we will get vote query only if the user has already voted for the post and if the user has not voted for the post it will return None 

   # we will enter else condition when the user has enetred vote.dir==0 and then we will check that if the user has already voted or not if voted then we will delete the vote and if not voted then we will create a new vote
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=409, detail="Vote already exists")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote created successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=404, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted successfully"}