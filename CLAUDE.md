# CLAUDE.md — Application de découpage de PDF

---

## Aperçu de l'objectif du projet

Application permettant à un utilisateur de :
- Télécharger un PDF de plusieurs pages.
- Sélectionner des pages individuelles ou des plages de pages.
- Extraire ces pages dans des fichiers PDF séparés.
- Télécharger tous les fichiers découpés dans un **zip**.
- Garantir la sécurité et la confidentialité des fichiers.

---

## Aperçu de l'architecture globale

| Couche      | Technologie             |
|-------------|-------------------------|
| Backend     | Python / FastAPI        |
| Frontend    | Vue 3 + Vite + TypeScript |
| Styling     | Tailwind CSS v3         |
| PDF parsing | pikepdf                 |
| Miniatures  | pdf2image (Poppler)     |
| Serveur     | Uvicorn (ASGI)          |

**Endpoints principaux :**
- `POST /upload` — Upload PDF, retourne `{ session_id, page_count }`
- `GET /thumbs/{session_id}` — Miniatures PNG de chaque page
- `POST /split` — Découpe et téléchargement en zip

**Structure du projet :**
```
appli_demo2/
├── backend/
│   ├── main.py
│   ├── routes/         # upload.py, thumbs.py, split.py
│   ├── services/       # pdf_service.py, thumb_service.py, crypto_service.py, cleanup.py
│   └── models.py
├── frontend/
│   └── src/
│       └── components/ # UploadZone.vue, PageGrid.vue, PageCard.vue, DownloadButton.vue
```

---

## Style visuel

- Interface **claire et minimaliste**.
- **Pas de mode sombre** pour le MVP.

---

## Contraintes et Politiques

- **NE JAMAIS exposer les clés API au client.**

### Configuration backend — variables d'environnement

**RÈGLE ABSOLUE : aucune valeur de configuration ne doit être hardcodée dans les modules backend.**

Toute valeur configurable (URLs, tailles limites, chemins, durées, résolutions, origines CORS…) doit :
1. Être déclarée dans `backend/.env` (et dans `backend/.env.example`).
2. Être chargée **uniquement** via `backend/config.py`, qui fait autorité pour toute la configuration.
3. Être importée depuis `config.py` dans les routes et services : `from config import MA_VARIABLE`.

Avant d'écrire un nouveau module ou d'ajouter une constante dans une route ou un service, **vérifier si la valeur est déjà définie dans `.env`**. Si une nouvelle variable est nécessaire, l'ajouter simultanément dans `.env`, `.env.example` et `config.py`.

Exemples de valeurs **interdites en dur** dans les modules :
- Chemins de répertoires (`/tmp/…`)
- Tailles limites (`10 * 1024 * 1024`)
- Origines CORS (`http://localhost:5173`)
- Durées d'expiration
- Résolutions d'image (DPI)

---

## Dépendances

- Préférer les **composants existants** plutôt que d'ajouter de nouvelles bibliothèques UI.

---

## Tests interface graphique

À la fin de chaque développement qui implique l'interface graphique :
- Tester avec le **MCP Puppeteer** : l'interface doit être responsive, fonctionnel et répondre au besoin développé.

---

## Documentation

- [PRD.md](./PRD.md) — Product Requirements Document
- [ARCHITECTURE.md](./ARCHITECTURE.md) — Architecture technique

---

## Context7

Utiliser **toujours Context7** pour la génération de code, les étapes de configuration ou d'installation, et la documentation de bibliothèque/API — sans attendre une demande explicite. Cela signifie utiliser automatiquement les outils MCP Context7 pour résoudre l'identifiant de bibliothèque et obtenir la documentation.

---

## Langue des spécifications

- Toutes les spécifications doivent être rédigées en **français**, y compris les specs OpenSpec (sections Purpose et Scenarios).
- Seuls les **titres de Requirements** restent en anglais avec les mots-clés `SHALL`/`MUST` pour la validation OpenSpec.
