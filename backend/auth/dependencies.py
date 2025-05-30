from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.db import SessionLocal
from backend.models import User

def get_db():
    db = SessionLocal() # 1. creating a new DB session (connecting to our DB)
    try:
        yield db # 2. We'll pass it to the route function (like a return, but context(database lifecycle) stays open)
    finally:
        db.close() # 3. After request completion, close the session (cleanup) 

def get_current_user(request: Request, db: Session = Depends(get_db)):
    session_id = request.cookies.get("session_id")
    if session_id is None:
        raise HTTPException(status_code=403, detail="Not authenticated.")
    user = db.get(User, session_id)
    if not user:
        raise HTTPException(status_code=403, detail="Invalid session.")
    return user
