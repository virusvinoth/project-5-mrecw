from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, utils


router = APIRouter(tags=["Auth"])
@router.post("/register", response_model=schemas.UserOut)

def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd = utils.hash_password(user.password)
    new_user = models.User(name=user.name, email=user.email,
    password_hash=hashed_pwd, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)

def login(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email ==
user.email).first()
    
    if not db_user or not utils.verify_password(user.password,
        db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = utils.create_access_token({"sub": db_user.email, "role":
    db_user.role})
    
    return {"access_token": token, "token_type": "bearer"}