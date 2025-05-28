#FASTAPI imports
from fastapi import FastAPI, Request, Header, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder

#Other imports
from uuid import uuid4
from typing import Annotated, Union
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from backend.db import SessionLocal
from backend.models import User
from passlib.hash import bcrypt

# Instantiate app
app = FastAPI()

# mounting static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal() # 1. creating a new DB session (connecting to our DB)
    try:
        yield db # 2. We'll pass it to the route function (like a return, but context(database lifecycle) stays open)
    finally:
        db.close() # 3. After request completion, close the session (cleanup) 

# Handle GET request to root
@app.get("/")
def read_home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/login")
def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup")
def show_signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup_user(request: Request, username: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):

    stmt = select(User).where(User.username == username)
    result = db.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        raise ValueError("User already exists.")
    else: 
        hashed_password = bcrypt.hash(password)
        user = User(username = username, email = email, password = hashed_password)
        db.add(user)
        db.commit()
        return templates.TemplateResponse("signup_success.html", {"request": request})