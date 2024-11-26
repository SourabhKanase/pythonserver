# schemas.py
from pydantic import BaseModel
from typing import Optional
from pydantic.types import conint

# class PostSchema(BaseModel):
#     title: str
#     content: str
#     published: bool = True

#     class Config:
#         orm_mode = True
class UserSchema(BaseModel):
    email: str
    password: str
    name: str        

class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    owner: Optional[UserSchema]

    class Config:
        orm_mode = True


class VoteSchema(BaseModel):
    post_id: int
    dir:conint(le=1)





class Respone(BaseModel):
    email: str
    password: str
    name: str

    class Config:
        orm_mode = True    


class LoginSchema(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id:Optional[int]=None