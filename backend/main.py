from fastapi import FastAPI
import auth, courses, payments, recommendations, database, models
models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="EdTech API")
app.include_router(auth.router, prefix="/auth")
app.include_router(courses.router, prefix="/courses")
app.include_router(payments.router, prefix="/payments")
app.include_router(recommendations.router, prefix="/recommend")
@app.get("/")

def home():
    return {"message": "EdTech API is running"}