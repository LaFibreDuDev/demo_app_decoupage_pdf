"""Thumbnail generation service: converts PDF pages to PNG images via pdf2image."""

import os
from pdf2image import convert_from_bytes

from config import TEMP_DIR, THUMB_DPI
from services.crypto_service import decrypt_file


def generate_thumbnails(session_id: str) -> list[str]:
    """Decrypt the session PDF and generate PNG thumbnails for each page.

    Returns a list of URL paths: ["/thumbs/{session_id}/1", ...]

    Uses on-disk cache: if thumbnails already exist, returns URLs without regenerating.

    Raises:
        FileNotFoundError if the session directory or encrypted PDF does not exist.
    """
    session_dir = os.path.join(TEMP_DIR, session_id)
    enc_path = os.path.join(session_dir, "original.pdf.enc")

    if not os.path.isdir(session_dir) or not os.path.isfile(enc_path):
        raise FileNotFoundError(f"Session not found: {session_id}")

    thumbs_dir = os.path.join(session_dir, "thumbs")

    # Return cached URLs if already generated
    if os.path.isdir(thumbs_dir) and len(os.listdir(thumbs_dir)) > 0:
        count = len(os.listdir(thumbs_dir))
        return [f"/thumbs/{session_id}/{n}" for n in range(1, count + 1)]

    os.makedirs(thumbs_dir, exist_ok=True)

    with open(enc_path, "rb") as f:
        encrypted = f.read()

    plaintext = decrypt_file(session_id, encrypted)

    images = convert_from_bytes(plaintext, dpi=THUMB_DPI)

    for i, image in enumerate(images, start=1):
        image.save(os.path.join(thumbs_dir, f"page_{i}.png"), format="PNG")

    return [f"/thumbs/{session_id}/{n}" for n in range(1, len(images) + 1)]
