## Why

La grille de sélection affiche actuellement de simples cases numérotées, ce qui oblige l'utilisateur à mémoriser mentalement le contenu de chaque page. Afficher une miniature visuelle de chaque page rend la sélection intuitive et sans ambiguïté.

## What Changes

- Le backend expose un nouvel endpoint `GET /thumbs/{session_id}` qui génère et retourne les miniatures PNG de chaque page du PDF.
- Les miniatures sont générées via `pdf2image` (Poppler), déjà présent dans les dépendances système.
- Le composant `PageCard.vue` affiche la miniature de la page à la place du simple numéro centré.
- Le composant `PageGrid.vue` récupère les URLs des miniatures depuis l'endpoint et les transmet à chaque `PageCard`.

## Capabilities

### New Capabilities

- `page-thumbnails` : endpoint backend `GET /thumbs/{session_id}` et service de génération de miniatures PNG par page (résolution configurable, cache par session).

### Modified Capabilities

- `page-selection` : le requirement "Affichage de la grille de pages après upload" change — les cases affichent désormais une miniature PNG à la place du numéro seul. Le numéro reste visible en superposition.

## Impact

- **Backend** : nouveau fichier `backend/routes/thumbs.py`, nouveau service `backend/services/thumb_service.py`, enregistrement de la route dans `main.py`.
- **Frontend** : `PageGrid.vue` — appel `GET /thumbs/{session_id}` après upload réussi, passage des URLs aux cards. `PageCard.vue` — affichage de l'image miniature + numéro en overlay.
- **Config** : nouvelle variable `THUMB_DPI` dans `.env` / `config.py` (résolution de génération).
- **Dépendances** : aucune nouvelle librairie — `pdf2image` et Poppler sont déjà requis.
- **Proxy Vite** : ajouter `/thumbs` dans `vite.config.ts`.
