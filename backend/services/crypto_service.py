"""AES-256 encryption/decryption for temporary PDF storage.

Keys are stored in memory only — never written to disk.
"""

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# In-memory key store: session_id -> bytes (32-byte AES-256 key)
_session_keys: dict[str, bytes] = {}


def generate_key(session_id: str) -> None:
    """Generate and store a new AES-256 key for a session."""
    _session_keys[session_id] = AESGCM.generate_key(bit_length=256)


def encrypt_file(session_id: str, plaintext: bytes) -> bytes:
    """Encrypt plaintext bytes for a session. Returns nonce + ciphertext."""
    key = _session_keys[session_id]
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return nonce + ciphertext


def decrypt_file(session_id: str, data: bytes) -> bytes:
    """Decrypt data (nonce + ciphertext) for a session. Returns plaintext."""
    key = _session_keys[session_id]
    aesgcm = AESGCM(key)
    nonce, ciphertext = data[:12], data[12:]
    return aesgcm.decrypt(nonce, ciphertext, None)


def delete_key(session_id: str) -> None:
    """Remove a session key from memory."""
    _session_keys.pop(session_id, None)
