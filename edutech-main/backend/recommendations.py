from fastapi import APIRouter

router = APIRouter(tags=["Recommendations"])

@router.get("/")
def recommend_courses():
    return [
        {"id": 1, "title": "Python Basics", "score": 0.95},
        {"id": 2, "title": "React for Beginners", "score": 0.90}
    ]
