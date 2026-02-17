# Architecture — Application de découpage de PDF

## Stack choisie

| Couche      | Technologie             | Version cible |
|-------------|-------------------------|---------------|
| Backend     | Python / FastAPI        | Python 3.11+  |
| Frontend    | Vue 3 + Vite + TypeScript | Vue 3.5+    |
| Styling     | Tailwind CSS            | v3            |
| PDF parsing | pikepdf                 | dernière      |
| Miniatures  | pdf2image (Poppler)     | dernière      |
| Serveur     | Uvicorn (ASGI)          | dernière      |

---

## Librairies backend

| Librairie    | Rôle                                                       |
|--------------|------------------------------------------------------------|
| `fastapi`    | Framework HTTP, gestion des routes et validation           |
| `uvicorn`    | Serveur ASGI pour exécuter FastAPI                         |
| `pikepdf`    | Lecture, découpage et écriture des fichiers PDF            |
| `pdf2image`  | Génération des miniatures PNG depuis les pages PDF         |
| `python-multipart` | Parsing des uploads `multipart/form-data`          |
| `cryptography` | Chiffrement AES des fichiers temporaires sur disque      |
| `zipfile`    | Création de l'archive zip (stdlib Python)                  |
| `uuid`       | Génération d'identifiants de session uniques (stdlib)      |

---

## Librairies frontend

| Librairie       | Rôle                                                    |
|-----------------|---------------------------------------------------------|
| `vue`           | Framework réactif, composants SFC                       |
| `vite`          | Bundler/dev server ultra-rapide                         |
| `typescript`    | Typage statique, utilisé dans tous les composants Vue   |
| `vue-tsc`       | Vérification de types sur les fichiers `.vue`           |
| `tailwindcss`   | Utilitaires CSS, responsive mobile/desktop              |

---

## Dépendances système

| Paquet          | Rôle                                                    |
|-----------------|---------------------------------------------------------|
| `libqpdf-dev`   | Dépendance native de pikepdf                            |
| `poppler-utils` | Rendu des pages PDF en images (requis par pdf2image)    |

Installation :
```bash
apt install libqpdf-dev poppler-utils
```

---

## Architecture des endpoints

### `POST /upload`
- Reçoit un fichier PDF via `multipart/form-data`
- Valide : type MIME (`application/pdf`), taille ≤ 10 Mo
- Stocke le fichier chiffré dans un répertoire de session temporaire
- Retourne : `{ session_id, page_count }`

### `GET /thumbs/{session_id}`
- Génère (ou retourne depuis cache) les miniatures PNG de chaque page
- Résolution : 150 dpi (compromis qualité/vitesse)
- Retourne : liste d'URL de miniatures `[ "/thumbs/{session_id}/page_{n}.png", … ]`

### `POST /split`
- Corps JSON : `{ session_id, selections: [ { pages: [1,3], name: "…" }, … ] }`
- Découpe le PDF déchiffré en mémoire avec pikepdf
- Renomme automatiquement : `originalfilename_page1-3.pdf`
- Crée un zip en mémoire, le retourne en streaming
- Supprime immédiatement les fichiers temporaires après envoi

---

## Structure de fichiers — répertoires temporaires

```
/tmp/pdf_splitter/
└── {session_id}/
    ├── original.pdf.enc     # PDF chiffré (AES-256)
    ├── key.bin              # Clé AES de session (en mémoire uniquement)
    └── thumbs/
        ├── page_1.png
        ├── page_2.png
        └── …
```

- Nettoyage automatique : job toutes les heures, suppression des sessions > 24h
- Suppression immédiate après téléchargement du zip

---

## Modèle de sécurité

### Validation à l'upload
- Type MIME vérifié côté serveur (pas seulement l'extension)
- Taille maximale : 10 Mo (rejetée avant écriture disque)
- Nom de fichier sanitisé (suppression des chemins, caractères spéciaux)

### Isolation des sessions
- Chaque upload reçoit un `session_id` UUID v4 aléatoire
- Les répertoires de session ne sont accessibles qu'via leur UUID
- Pas de listage des sessions côté API

### Chiffrement temporaire
- Fichier PDF stocké chiffré avec AES-256 (bibliothèque `cryptography`)
- La clé de déchiffrement réside uniquement en mémoire (non écrite sur disque)
- Déchiffrement en mémoire uniquement au moment du découpage

### Nettoyage
- Suppression immédiate après streaming du zip
- Nettoyage planifié (cron ou tâche asyncio) : sessions > 24h supprimées
- Aucun log des contenus de fichiers

---

## Structure du projet

```
appli_demo2/
├── backend/
│   ├── main.py              # Point d'entrée FastAPI, déclaration des routes
│   ├── routes/
│   │   ├── upload.py        # POST /upload
│   │   ├── thumbs.py        # GET /thumbs/{session_id}
│   │   └── split.py         # POST /split
│   ├── services/
│   │   ├── pdf_service.py   # Logique pikepdf (découpage, comptage pages)
│   │   ├── thumb_service.py # Logique pdf2image (génération miniatures)
│   │   ├── crypto_service.py# Chiffrement/déchiffrement AES des fichiers
│   │   └── cleanup.py       # Nettoyage automatique des sessions expirées
│   ├── models.py            # Schémas Pydantic (SplitRequest, UploadResponse…)
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── src/
│       ├── vite-env.d.ts
│       ├── main.ts
│       ├── App.vue
│       └── components/
│           ├── UploadZone.vue    # Drag & drop, bouton, validation
│           ├── PageGrid.vue      # Grille de miniatures + sélection
│           ├── PageCard.vue      # Carte d'une page (miniature + checkbox)
│           └── DownloadButton.vue# Déclenchement du split et téléchargement
│
├── PRD.md
├── ARCHITECTURE.md
└── discussions.md
```
