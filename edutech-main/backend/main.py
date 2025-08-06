from fastapi import FastAPI
import auth, courses, payments, recommendations, database, models,ml_suggest,chatmodel
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="EdTech API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix="/auth")
app.include_router(courses.router, prefix="/courses")
app.include_router(payments.router, prefix="/payments")
app.include_router(recommendations.router, prefix="/recommend")
app.include_router(ml_suggest.router, prefix="/suggest")

app.include_router(chatmodel.router,prefix="/ML")


@app.get("/")
def home():
    return {"message": "EdTech API is running"}
