"""Periodic cleanup of expired session directories.

Sessions older than SESSION_TTL_HOURS are deleted automatically.
The cleanup loop runs every hour via asyncio.
"""

import asyncio
import logging
import os
import shutil
import time

from config import SESSION_TTL_HOURS, TEMP_DIR
from services.crypto_service import delete_key

logger = logging.getLogger(__name__)

_TTL_SECONDS = SESSION_TTL_HOURS * 3600
_CHECK_INTERVAL_SECONDS = 3600  # run every hour


def _cleanup_expired_sessions() -> int:
    """Delete session directories older than TTL. Returns count of deleted sessions."""
    if not os.path.isdir(TEMP_DIR):
        return 0

    now = time.time()
    deleted = 0

    for session_id in os.listdir(TEMP_DIR):
        session_dir = os.path.join(TEMP_DIR, session_id)
        if not os.path.isdir(session_dir):
            continue

        age = now - os.path.getmtime(session_dir)
        if age >= _TTL_SECONDS:
            shutil.rmtree(session_dir, ignore_errors=True)
            delete_key(session_id)
            deleted += 1
            logger.info("Session expirée supprimée : %s (âge : %.1f h)", session_id, age / 3600)

    return deleted


async def cleanup_loop() -> None:
    """Asyncio background task: run cleanup every hour."""
    while True:
        try:
            deleted = _cleanup_expired_sessions()
            if deleted:
                logger.info("Nettoyage : %d session(s) supprimée(s).", deleted)
        except Exception:
            logger.exception("Erreur lors du nettoyage des sessions.")
        await asyncio.sleep(_CHECK_INTERVAL_SECONDS)
