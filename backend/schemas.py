from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[str] = "student"
class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
class Config:
    orm_mode = True
class Token(BaseModel):
    access_token: str
    token_type: str
class CourseCreate(BaseModel):
    title: str
    description: str
    price: float
class LessonCreate(BaseModel):
    title: str
    video_url: str
