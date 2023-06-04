# import requests
import requests
from dotenv import load_dotenv
import json
import os
import base64
import datetime
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

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"

load_dotenv()

app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend())

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

DB_SESSION = None

from application.handlers import * # noqa

#settings = config.get_settings()

@app.on_event("startup")
def on_startup():
    print("Hello world")
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@app.get("/users")
def users_list_view():
    q = User.objects.all().limit(10)
    return list(q)

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

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

 
class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

   
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    
    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }
    
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True
    
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers
    
    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
   
    def get_artist(self, _id):
        return self.get_resource(_id, resource_type="artists")  
    
    def base_search(self, query_params):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        print(lookup_url)
        r = requests.get(lookup_url, headers=headers)
        print(r.status_code)
        if r.status_code not in range(200, 209):
            return {}
        return r.json()
    
    def search(self, query=None, search_type="artists"):
        if query == None:
            raise Exception("A query is required")
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k, v in query.items()])
        query_params = urlencode({"q": query , "type": search_type.lower()})
        print(query_params)
        return self.base_search(query_params)

   

spotify = SpotifyAPI(client_id, client_secret)    
#print(spotify.perform_auth())
print(spotify.get_access_token())
#print(spotify.search("Time", search_type="Track"))
#print(spotify.get_artist("0TnOYISbd1XYRBk9myaseg"))
#access_token = spotify.access_token
#print(access_token)
#print(spotify.search({"track": "Time"}, search_type="track"))






