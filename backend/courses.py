from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas
router = APIRouter(tags=["Courses"])
@router.post("/", response_model=schemas.CourseCreate)

def create_course(course: schemas.CourseCreate, db: Session =
Depends(database.get_db)):
    new_course = models.Course(**course.dict(), instructor_id=1) # Dummy instructor
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.get("/")
def list_courses(db: Session = Depends(database.get_db)):
    return db.query(models.Course).all()