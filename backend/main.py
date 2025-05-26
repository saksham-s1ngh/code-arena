#FASTAPI imports
from fastapi import FastAPI, Request, Header, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder

#Other imports
from uuid import uuid4
from typing import Annotated, Union

# Instantiate app
app = FastAPI()

# mounting static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

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

# @app.get("/items/{id}", response_class = HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse(
#         request=request, name="item.html", context={"id": id}
#     )