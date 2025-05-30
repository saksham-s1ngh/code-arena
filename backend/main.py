#FASTAPI imports
from fastapi import FastAPI, Request, Form, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

#Other imports
from uuid import uuid4
from typing import Annotated, Union
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from backend.db import SessionLocal
from backend.models import User
from passlib.hash import bcrypt
from pathlib import Path

# within project imports
from backend.auth.dependencies import get_db, get_current_user

# Instantiate app
app = FastAPI()

# this statement will help resolve absolute path to project root
BASE_DIR = Path(__file__).resolve().parent.parent 

templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

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
    
@app.post("/login")
def login_user(request: Request, response: Response ,username: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):
    stmt = select(User).where(User.username == username)
    result = db.execute(stmt) # cursor object that hasn't been unpacked
    user = result.scalar_one_or_none()
    if user:
        hashed_password = bcrypt.hash(password)
        pass_check = bcrypt.verify(hashed_password, user.password)
        if pass_check:
            # TODO - currently using user.id as session value. Randomize or hash this!
            response.set_cookie(key="session_id", value=str(user.id), httponly=True) 
            return templates.TemplateResponse("dashboard.html", {"request": request})
        else:
            # have an error message displayed on the login page with "Incorrect password!" message
            return templates.TemplateResponse("login.html", {
                "request": request,
                "error": "Incorrect password!"
                }) # from here, we can access {{ error }} through Jinja
    else:
        raise ValueError(f"No account found for {username}!")
    
@app.get("/dashboard")
def get_dashboard(request: Request, user: User = Depends(get_current_user)):
    # session_id = request.cookies.get("session_id")
    # if session_id is None:
    #     return RedirectResponse("/login")
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})