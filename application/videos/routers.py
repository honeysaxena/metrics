from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from application.shortcuts import render, redirect
from application.users.decorators import login_required
from application import utils
from application.videos.schemas import VideoCreateSchema
from application.videos.models import Video
from application.db import SessionLocal

session = SessionLocal()

router = APIRouter(
    prefix='/videos'
)

#@router.get("/", response_class=HTMLResponse)
#def video_list_view(request: Request):
#    return render(request, "songs/list.html", {})

@router.get("/create", response_class=HTMLResponse)
@login_required
def video_create_view(request: Request):
    return render(request, "videos/create.html", {})

@router.post("/create", response_class=HTMLResponse)
@login_required
def video_create_post_view(request: Request, title: str = Form(...), url: str = Form(...)):
    raw_data = {
        "title": title,
        "url": url,
        "user_id": request.user.username
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, VideoCreateSchema)
    context = {
        "data": data,
        "errors": errors,
        "url": url
    }
    if len(errors) > 0:
        return render(request, "videos/create.html", context, status_code=400)
    redirect_path = data.get('path') or "/videos/create"
    return redirect(redirect_path)
    #return render(request, "videos/create.html", context)

@router.get("/", response_class=HTMLResponse)
def video_list_view(request: Request):
    q = session.query(Video).all()
    context = {
        "object_list": q
    }
    return render(request, "videos/list.html", context)

@router.get("/detail", response_class=HTMLResponse)
def song_detail_view(request: Request):
    return render(request, "videos/detail.html", {})

