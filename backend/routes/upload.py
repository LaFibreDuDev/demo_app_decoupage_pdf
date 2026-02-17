from fastapi import APIRouter, UploadFile, File

from models import UploadResponse
from services.pdf_service import save_upload

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    session_id, page_count = await save_upload(file)
    return UploadResponse(session_id=session_id, page_count=page_count)
