#FASTAPI imports
from fastapi import FastAPI, Request, Form, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

#Other imports
from uuid import uuid4
from typing import Annotated, Union
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from backend.db import SessionLocal
from backend.models import User
from passlib.hash import bcrypt
from pathlib import Path

# within project imports
from backend.auth.dependencies import get_db, get_current_user
from backend.core.room_manager import room_manager


# Instantiate app
app = FastAPI()

# this statement will help resolve absolute path to project root
BASE_DIR = Path(__file__).resolve().parent.parent 

templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Handle GET request to root
@app.get("/")
def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/login")
def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup")
def show_signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup_user(
    request: Request, 
    username: Annotated[str, Form()], 
    email: Annotated[str, Form()], 
    password: Annotated[str, Form()], 
    db: Session = Depends(get_db)
    ):

    # Check username
    stmt = select(User).where(User.username == username)
    result = db.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": f"User with username \'{username}\' already exists.",
            "username": username
        })
    
    # Check email
    stmt = select(User).where(User.email == email)
    if db.execute(stmt).scalar_one_or_none():
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": f"An account with '{email}' already exists.",
            "username": username,
            "email": email
        })

    hashed_password = bcrypt.hash(password)
    new_user = User(username = username, email = email, password = hashed_password)
    db.add(new_user)
    try :
        db.commit()
    except IntegrityError:
        db.rollback()
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error": "That username or email is already registered.", 
            "username": username,
            "email": email
        })
    return templates.TemplateResponse("signup_success.html", {"request": request})
    
@app.post("/login")
def login_user(request: Request, response: Response ,username: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):
    stmt = select(User).where(User.username == username)
    result = db.execute(stmt) # cursor object that hasn't been unpacked
    user = result.scalar_one_or_none()
    if user:
        pass_check = bcrypt.verify(password, user.password)
        if pass_check:
            # TODO - currently using user.id as session value. Randomize or hash this!
            response.set_cookie(key="session_id", value=str(user.id), httponly=True) 
            return templates.TemplateResponse("dashboard.html", {
                "request": request,
                "user": user
                })
        else:
            # have an error message displayed on the login page with "Incorrect password!" message
            return templates.TemplateResponse("login.html", {
                "request": request,
                "error": "Incorrect password!",
                "username": username
                }) # from here, we can access {{ error }} through Jinja
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": f"No account found for {username}",
            "username": username
        })
    
@app.get("/dashboard")
def get_dashboard(request: Request, user: User = Depends(get_current_user)):
    # session_id = request.cookies.get("session_id")
    # if session_id is None:
    #     return RedirectResponse("/login")
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

@app.get("/logout")
def get_logout(response: Response):
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("session_id")
    return response

@app.post("/create-room")
def create_room(request: Request, question_url: Annotated[str, Form()], user: User = Depends(get_current_user)):
    room_id = room_manager.create_room(user, question_url)
    return RedirectResponse(url=f"/room/{room_id}", status_code=303)

@app.get("/room/{room_id}")
def room_page(request: Request, room_id: str, user: User = Depends(get_current_user)):
    room = room_manager.get_room(room_id)
    if not room:
        return templates.TemplateResponse("404.html", {"request": request})
    return templates.TemplateResponse("room.html", {
        "request": request, 
        "room": room, 
        "room_id": room_id,
        "user": user
        })

@app.get("/room")
def redirect_to_room(room_id: str):
    return RedirectResponse(url=f"/room/{room_id}", status_code=303)