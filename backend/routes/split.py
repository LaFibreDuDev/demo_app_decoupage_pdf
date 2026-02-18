import io
import os
import zipfile

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from config import TEMP_DIR
from models import SplitRequest
from services.pdf_service import split_pdf, split_pdf_separate

router = APIRouter()


@router.post("/split")
async def split_pdf_route(request: SplitRequest):
    session_dir = os.path.join(TEMP_DIR, request.session_id)
    if not os.path.isdir(session_dir):
        raise HTTPException(status_code=404, detail="Session introuvable ou expirée.")

    if not request.pages:
        raise HTTPException(status_code=400, detail="Aucune page sélectionnée.")

    zip_buffer = io.BytesIO()
    try:
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            if request.output_mode == "separate":
                entries = split_pdf_separate(
                    request.session_id, request.original_filename, request.pages
                )
                for pdf_bytes, pdf_filename in entries:
                    zf.writestr(pdf_filename, pdf_bytes)
            else:
                pdf_bytes, pdf_filename = split_pdf(
                    request.session_id, request.original_filename, request.pages
                )
                zf.writestr(pdf_filename, pdf_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    zip_buffer.seek(0)

    zip_filename = f"{request.original_filename}_split.zip"

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{zip_filename}"'},
    )
