from fastapi import APIRouter
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
from transformers import PreTrainedModel, TrainingArguments

router = APIRouter(tags=["ML"])

# Load sentence-transformer model (lightweight)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Sample course data (can be fetched from DB)
with open("course_data.json", "r") as f:
    course_data = json.load(f)

course_titles = [course["title"] for course in course_data]
course_embeddings = embedder.encode(course_titles, convert_to_tensor=False)

# FAISS Index
dimension = course_embeddings[0].shape[0]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(course_embeddings))

class CourseRequest(BaseModel):
    title: str
    top_k: int = 3

@router.post("/generate")
async def suggest_related_courses(request: CourseRequest):
    embedding = embedder.encode([request.title])[0]
    distances, indices = index.search(np.array([embedding]), k=request.top_k)
    
    suggestions = [course_titles[i] for i in indices[0]]
    return {"suggestions": suggestions}
