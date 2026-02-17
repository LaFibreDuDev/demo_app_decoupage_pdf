## Why

L'application n'a pas encore de point d'entrée fonctionnel : l'utilisateur ne peut pas encore envoyer un fichier PDF au backend. Sans cette première brique, aucune fonctionnalité de découpage ne peut être testée ni livrée. Le MVP commence ici.

## What Changes

- Ajout d'un composant Vue `UploadZone` permettant à l'utilisateur de sélectionner un fichier PDF via un bouton (click).
- Validation côté client : type MIME `application/pdf` et taille maximale de 10 Mo.
- Appel à l'endpoint `POST /upload` du backend FastAPI.
- Affichage d'un retour visuel : état de chargement, erreur de validation, succès avec le nombre de pages retourné.
- Endpoint backend `POST /upload` : réception du fichier, validation serveur, génération d'un `session_id`, stockage temporaire du PDF, retour `{ session_id, page_count }`.

## Capabilities

### New Capabilities

- `pdf-upload`: Composant frontend d'upload de fichier PDF avec validation type/poids et feedback utilisateur ; endpoint backend `/upload` qui reçoit, valide et stocke le PDF, retournant un `session_id` et le nombre de pages.

### Modified Capabilities

<!-- Aucune spec existante à modifier pour le MVP -->

## Impact

- **Frontend** : nouveau composant `UploadZone.vue` dans `frontend/src/components/`.
- **Backend** : nouvelle route `backend/routes/upload.py`, service `backend/services/pdf_service.py` (fonction d'upload/validation).
- **Dépendances** : `pikepdf` (déjà prévu), `python-multipart` pour FastAPI file upload.
- **Pas de breaking changes** : première fonctionnalité du projet.
