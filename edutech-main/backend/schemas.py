from pydantic import BaseModel, EmailStr
from typing import List, Optional


# ----- USER SCHEMAS -----
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
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


# ----- COURSE SCHEMAS -----
class CourseCreate(BaseModel):
    title: str
    description: str
    price: float
    # Optional: add instructor_id if needed
    


class CourseOut(BaseModel):
    id: int
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True


# ----- LESSON SCHEMAS -----
class LessonCreate(BaseModel):
    title: str
    video_url: str
    course_id: int


class LessonOut(BaseModel):
    id: int
    title: str
    video_url: str
    course_id: int

    class Config:
        orm_mode = True


# ----- Optional: Nested Course with Lessons -----
class CourseWithLessons(BaseModel):
    id: int
    title: str
    description: str
    price: float
    lessons: List[LessonOut] = []

    class Config:
        orm_mode = True

