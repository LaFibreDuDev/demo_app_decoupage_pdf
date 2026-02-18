"""AES-256 encryption/decryption for temporary PDF storage.

Keys are derived on-the-fly via HKDF(SESSION_SECRET, session_id).
No key is ever stored in memory or on disk, making the approach safe
for multi-worker deployments: any worker can derive the same key for
a given session without inter-process communication.
"""

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

from config import SESSION_SECRET


def _derive_key(session_id: str) -> bytes:
    """Derive a deterministic 256-bit AES key from SESSION_SECRET + session_id."""
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=session_id.encode(),
    )
    return hkdf.derive(SESSION_SECRET)


def generate_key(session_id: str) -> None:
    """No-op — kept for API compatibility. Key is derived on demand."""
    pass


def encrypt_file(session_id: str, plaintext: bytes) -> bytes:
    """Encrypt plaintext bytes for a session. Returns nonce + ciphertext."""
    key = _derive_key(session_id)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return nonce + ciphertext


def decrypt_file(session_id: str, data: bytes) -> bytes:
    """Decrypt data (nonce + ciphertext) for a session. Returns plaintext."""
    key = _derive_key(session_id)
    aesgcm = AESGCM(key)
    nonce, ciphertext = data[:12], data[12:]
    return aesgcm.decrypt(nonce, ciphertext, None)


def delete_key(session_id: str) -> None:
    """No-op — kept for API compatibility. Nothing to delete with key derivation."""
    pass
