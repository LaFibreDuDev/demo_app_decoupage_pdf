"""PDF handling: validation, page counting, encrypted storage."""

import os
import uuid
import pikepdf
from fastapi import UploadFile, HTTPException

from config import TEMP_DIR, UPLOAD_MAX_SIZE_BYTES, UPLOAD_MAX_SIZE_MB
from services.crypto_service import generate_key, encrypt_file


async def save_upload(file: UploadFile) -> tuple[str, int]:
    """Validate, count pages, encrypt and store the uploaded PDF.

    Returns:
        (session_id, page_count)

    Raises:
        HTTPException 400 if file is not a valid PDF.
        HTTPException 413 if file exceeds 10 Mo.
    """
    content = await file.read()

    if len(content) > UPLOAD_MAX_SIZE_BYTES:
        raise HTTPException(status_code=413, detail=f"Fichier trop volumineux (max {UPLOAD_MAX_SIZE_MB} Mo).")

    if not content.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="Fichier invalide : ce n'est pas un PDF.")

    # Count pages using pikepdf (also validates the PDF structure)
    try:
        with pikepdf.open(__import__("io").BytesIO(content)) as pdf:
            page_count = len(pdf.pages)
    except pikepdf.PdfError:
        raise HTTPException(status_code=400, detail="Fichier invalide : ce n'est pas un PDF.")

    session_id = str(uuid.uuid4())
    session_dir = os.path.join(TEMP_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)

    generate_key(session_id)
    encrypted = encrypt_file(session_id, content)

    with open(os.path.join(session_dir, "original.pdf.enc"), "wb") as f:
        f.write(encrypted)

    return session_id, page_count
