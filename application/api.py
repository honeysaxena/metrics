import requests
from pathlib import Path
from urllib.parse import urlencode
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from cassandra.cqlengine.management import sync_table
from application.users.models import User
from application import config, db, utils
from application.users.schemas import UserSignupSchema, UserLoginSchema
from pydantic.error_wrappers import ValidationError
from application.shortcuts import render, redirect
from application.users.decorators import login_required
from application.users.backends import JWTCookieBackend
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires
from application.videos.models import Video
from application.videos.routers import router as video_router
from application.config import get_settings
from application.users.models import Base
from application.db import engine


Base.metadata.create_all(bind=engine)


DB_SESSION = None

BASE_DIR = Path(__file__).resolve().parent
#TEMPLATE_DIR = BASE_DIR / "templates"


app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend())
app.include_router(video_router)

#templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


from application.handlers import * # noqa

#settings = config.get_settings()

#@app.on_event("startup")
#def on_startup():
#    print("Hello world")
#    global DB_SESSION
#    DB_SESSION = db.get_session()
#    sync_table(User)
#    sync_table(Video)


@app.get("/users")
def users_list_view():
    q = User.objects.all().limit(10)
    return list(q)


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/home", response_class=HTMLResponse)
async def homepage(request: Request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html', {}, status_code=200)
    response = render(request, "home.html", {})
    #response = render(request, 'home.html', {})
    '''
    if len(cookies.keys()) > 0:
        for k, v in cookies.items():
            response.set_cookie(key='test', value='123', httponly=True)
    for key in request.cookies.keys():
        response.delete_cookie(key)
    '''    
    return response

@app.get("/account", response_class=HTMLResponse)
@login_required
async def account_view(request: Request):
    '''
    Hello user
    '''
    context = {}
    return render(request, "account.html", context)
   
        
@app.get("/login", response_class=HTMLResponse)
async def login_get_view(request: Request):
    session_id  = request.cookies.get("session_id") or None
    return render(request, "login.html", {"logged_in": session_id is not None})

@app.post("/login", response_class=HTMLResponse)
async def login_post_view(request: Request, email: str=Form(...), password: str=Form(...)):
    raw_data = {
        "email": email,
        "password": password,
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, UserLoginSchema)
    context = { 
        "data": data, 
        "errors": errors,
        
        }
    if len(errors) > 0:
        return render(request, "login.html", context,  status_code=400)
    print(data)
    return redirect("/home", cookies=data)

@app.get("/signup", response_class=HTMLResponse)
async def signup_get_view(request: Request):
    return render(request, "signup.html", {})

@app.post("/signup", response_class=HTMLResponse)
async def signup_post_view(request: Request, email: str=Form(...), password: str=Form(...), confirm_password: str=Form(...)):
    print(email, password)
    raw_data = {
        "email": email,
        "password": password,
        "confirm_password": confirm_password
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, UserSignupSchema)
    context = {
        "data": data,
        "errors": errors
        } 
    if len(errors) > 0:
        return render(request, "signup.html", context, status_code=400)       
    return redirect("/login")

@app.get("/typer")
async def redirect_typer():
    return RedirectResponse("https://typer.tiangolo.com")





