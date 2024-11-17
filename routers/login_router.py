from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from models.models import get_db, User

router = APIRouter()

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful! Redirecting to dashboard..."}