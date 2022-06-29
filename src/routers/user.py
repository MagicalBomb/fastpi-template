from fastapi import APIRouter, Depends
from models.base import SessionLocal
from models import User
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/user', name="新建用户")
def test_user(db: Session = Depends(get_db)):
    user = User(email="test@email.com")
    db.add(user)
    db.commit()
