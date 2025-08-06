from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))
    role = Column(String(50), default="student")
    created_at = Column(DateTime, default=func.now())


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    price = Column(Float)

    # FIX: back_populates must match the 'course' relationship in Lesson
    lessons = relationship("Lesson", back_populates="course")

    
class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    video_url = Column(String(500))
    course_id = Column(Integer, ForeignKey("courses.id"))

    course = relationship("Course", back_populates="lessons")
