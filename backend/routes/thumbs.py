"""Routes for thumbnail generation and serving."""

import os
from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse

from config import TEMP_DIR
from services.thumb_service import generate_thumbnails

router = APIRouter()


@router.get("/thumbs/{session_id}", response_class=JSONResponse)
async def list_thumbnails(session_id: str):
    try:
        urls = generate_thumbnails(session_id)
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"detail": "Session introuvable."})
    return {"urls": urls}


@router.get("/thumbs/{session_id}/{page}")
async def get_thumbnail(session_id: str, page: int):
    thumb_path = os.path.join(TEMP_DIR, session_id, "thumbs", f"page_{page}.png")
    if not os.path.isfile(thumb_path):
        return JSONResponse(status_code=404, content={"detail": "Miniature introuvable."})
    return FileResponse(thumb_path, media_type="image/png")
