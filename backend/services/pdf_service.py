"""PDF handling: validation, page counting, encrypted storage, splitting."""

import io
import os
import re
import uuid
import zipfile
import shutil
import pikepdf
from fastapi import UploadFile, HTTPException

from config import TEMP_DIR, UPLOAD_MAX_SIZE_BYTES, UPLOAD_MAX_SIZE_MB
from services.crypto_service import generate_key, encrypt_file, decrypt_file, delete_key


def _sanitize_filename(name: str) -> str:
    """Return the base name without extension, keeping only safe characters."""
    basename = os.path.splitext(os.path.basename(name))[0]
    return re.sub(r"[^\w\-]", "_", basename)


async def save_upload(file: UploadFile) -> tuple[str, int, str]:
    """Validate, count pages, encrypt and store the uploaded PDF.

    Returns:
        (session_id, page_count, original_filename)

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
        with pikepdf.open(io.BytesIO(content)) as pdf:
            page_count = len(pdf.pages)
    except pikepdf.PdfError:
        raise HTTPException(status_code=400, detail="Fichier invalide : ce n'est pas un PDF.")

    original_filename = _sanitize_filename(file.filename or "document")

    session_id = str(uuid.uuid4())
    session_dir = os.path.join(TEMP_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)

    generate_key(session_id)
    encrypted = encrypt_file(session_id, content)

    with open(os.path.join(session_dir, "original.pdf.enc"), "wb") as f:
        f.write(encrypted)

    return session_id, page_count, original_filename


def split_pdf(session_id: str, original_filename: str, pages: list[int]) -> tuple[bytes, str]:
    """Decrypt session PDF, extract requested pages, return (pdf_bytes, output_filename).

    Raises:
        ValueError if a page number is out of range.
    """
    session_dir = os.path.join(TEMP_DIR, session_id)
    enc_path = os.path.join(session_dir, "original.pdf.enc")

    with open(enc_path, "rb") as f:
        encrypted = f.read()

    plaintext = decrypt_file(session_id, encrypted)

    with pikepdf.open(io.BytesIO(plaintext)) as pdf:
        total_pages = len(pdf.pages)

        for p in pages:
            if p < 1 or p > total_pages:
                raise ValueError(f"Numéro de page invalide : {p} (le PDF a {total_pages} pages).")

        new_pdf = pikepdf.Pdf.new()
        for p in pages:
            new_pdf.pages.append(pdf.pages[p - 1])

        output = io.BytesIO()
        new_pdf.save(output)
        pdf_bytes = output.getvalue()

    page_str = "-".join(str(p) for p in pages)
    output_filename = f"{original_filename}_page{page_str}.pdf"

    return pdf_bytes, output_filename


def split_pdf_separate(session_id: str, original_filename: str, pages: list[int]) -> list[tuple[bytes, str]]:
    """Decrypt session PDF, extract each requested page as a separate PDF.

    Returns:
        List of (pdf_bytes, output_filename) tuples, one per page.

    Raises:
        ValueError if a page number is out of range.
    """
    session_dir = os.path.join(TEMP_DIR, session_id)
    enc_path = os.path.join(session_dir, "original.pdf.enc")

    with open(enc_path, "rb") as f:
        encrypted = f.read()

    plaintext = decrypt_file(session_id, encrypted)

    results = []
    with pikepdf.open(io.BytesIO(plaintext)) as pdf:
        total_pages = len(pdf.pages)

        for p in pages:
            if p < 1 or p > total_pages:
                raise ValueError(f"Numéro de page invalide : {p} (le PDF a {total_pages} pages).")

        for p in pages:
            new_pdf = pikepdf.Pdf.new()
            new_pdf.pages.append(pdf.pages[p - 1])

            output = io.BytesIO()
            new_pdf.save(output)
            pdf_bytes = output.getvalue()

            output_filename = f"{original_filename}_page{p}.pdf"
            results.append((pdf_bytes, output_filename))

    return results
