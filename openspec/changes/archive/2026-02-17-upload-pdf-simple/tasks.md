## 1. Infrastructure Backend

- [x] 1.1 Créer la structure de répertoires backend (`routes/`, `services/`, `models.py`, `main.py`, `requirements.txt`)
- [x] 1.2 Écrire `requirements.txt` avec les dépendances du MVP (`fastapi`, `uvicorn`, `python-multipart`, `pikepdf`, `cryptography`)
- [x] 1.3 Créer `backend/main.py` : app FastAPI, inclusion de la route upload, CORS configuré pour le dev

## 2. Backend — Service et Route Upload

- [x] 2.1 Créer `backend/services/crypto_service.py` : chiffrement/déchiffrement AES-256 d'un fichier, stockage de la clé en mémoire (dict global `session_keys`)
- [x] 2.2 Créer `backend/services/pdf_service.py` : fonction `save_upload(file, session_id)` — validation magic bytes `%PDF-`, comptage pages avec pikepdf, stockage chiffré dans `/tmp/pdf_splitter/{session_id}/original.pdf.enc`
- [x] 2.3 Créer `backend/models.py` : modèle Pydantic `UploadResponse(session_id: str, page_count: int)`
- [x] 2.4 Créer `backend/routes/upload.py` : endpoint `POST /upload` — validation taille ≤ 10 Mo, appel `pdf_service.save_upload`, retour `UploadResponse`

## 3. Infrastructure Frontend

- [x] 3.1 Créer la structure frontend avec Vite (`npm create vite@latest frontend -- --template vue`)
- [x] 3.2 Installer Tailwind CSS v3 et configurer `tailwind.config.js` et `vite.config.js` (proxy `/api` → `http://localhost:8000`)
- [x] 3.3 Créer `frontend/src/App.vue` minimal avec état `sessionId` et `pageCount`

## 4. Frontend — Composant UploadZone

- [x] 4.1 Créer `frontend/src/components/UploadZone.vue` avec bouton de sélection de fichier (input file caché, accepte `application/pdf`)
- [x] 4.2 Implémenter la validation client : type MIME `application/pdf` et taille ≤ 10 Mo avec messages d'erreur
- [x] 4.3 Implémenter l'appel `POST /api/upload` via `fetch`, avec état de chargement (bouton désactivé + spinner)
- [x] 4.4 Afficher le feedback de succès ("PDF chargé — X page(s)") et émettre `upload-success` avec `{ session_id, page_count }` vers `App.vue`
- [x] 4.5 Afficher les erreurs serveur (4xx/5xx) à l'utilisateur
