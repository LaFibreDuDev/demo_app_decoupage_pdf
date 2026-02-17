import io
import zipfile

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from models import SplitRequest
from services.crypto_service import _session_keys
from services.pdf_service import split_pdf

router = APIRouter()


@router.post("/split")
async def split_pdf_route(request: SplitRequest):
    if request.session_id not in _session_keys:
        raise HTTPException(status_code=404, detail="Session introuvable ou expirée.")

    if not request.pages:
        raise HTTPException(status_code=400, detail="Aucune page sélectionnée.")

    try:
        pdf_bytes, pdf_filename = split_pdf(
            request.session_id, request.original_filename, request.pages
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(pdf_filename, pdf_bytes)
    zip_buffer.seek(0)

    zip_filename = f"{request.original_filename}_split.zip"

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{zip_filename}"'},
    )
