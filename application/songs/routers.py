from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from application.shortcuts import render

router = APIRouter(
    prefix='/videos'
)
  

@router.get("/", response_class=HTMLResponse)
def song_list_view(request: Request):
    return render(request, "songs/list.html", {})

@router.get("/detail", response_class=HTMLResponse)
def song_detail_view(request: Request):
    return render(request, "songs/detail.html", {})