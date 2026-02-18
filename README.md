# PDF Splitter

Application web permettant de découper un PDF en fichiers séparés et de les télécharger dans un zip.

## Fonctionnalités

- Upload d'un PDF via drag & drop ou bouton (max 10 Mo)
- Aperçu des pages sous forme de miniatures
- Sélection de pages individuelles ou de plages de pages
- Découpage et téléchargement automatique en zip
- Sécurité : fichiers chiffrés temporairement (AES-256), supprimés après téléchargement ou 24h

## Stack technique

| Couche      | Technologie                     |
|-------------|---------------------------------|
| Backend     | Python 3.11+ / FastAPI          |
| Frontend    | Vue 3 + Vite + TypeScript + Tailwind CSS v3 |
| PDF parsing | pikepdf                         |
| Miniatures  | pdf2image (Poppler)             |
| Serveur     | Uvicorn (ASGI)                  |

---

## Prérequis

### Système

```bash
apt install libqpdf-dev poppler-utils
```

### Python

- Python 3.11+
- `pip` ou `venv`

### Node.js

- Node.js 18+ avec `npm`

---

## Lancement du projet

### 1. Backend (FastAPI)

```bash
cd backend

# Créer et activer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env si besoin (ports, chemins, limites…)

# Si jamais l'application est déjà lancée et que tu veux faire du ménage :
pkill -f "uvicorn main:app"

# Démarrer le serveur
python3 -m uvicorn main:app --reload --port 8000 &
```

L'API est disponible sur **http://localhost:8000**.
Documentation Swagger auto-générée : **http://localhost:8000/docs**

### 2. Frontend (Vue 3 + Vite + TypeScript)

Dans un second terminal :

```bash
cd frontend

# Installer les dépendances
npm install

# Démarrer le serveur de développement
npm run dev
```

L'interface est disponible sur **http://localhost:5173**.

---

## Lancement avec Docker (dev)

> Alternative à la méthode manuelle. Le hot-reload fonctionne pour le backend (uvicorn `--reload`) et le frontend (HMR Vite).

### Prérequis

- Docker Engine 24+
- Docker Compose v2

### Démarrage

```bash
# Configurer les variables d'environnement (si pas encore fait)
cp backend/.env.example backend/.env

# Construire les images et démarrer tous les services
docker compose -f docker-compose.dev.yml up --build
```

Les services sont accessibles via le reverse proxy Nginx sur le port **8080** :

| URL | Description |
|-----|-------------|
| http://frontend.localhost:8080 | Interface de l'application |
| http://backend.localhost:8080/docs | Documentation Swagger de l'API |

> `*.localhost` se résout automatiquement vers `127.0.0.1` dans la plupart des navigateurs et systèmes.
> Si ce n'est pas le cas, ajouter dans `/etc/hosts` :
> ```
> 127.0.0.1  frontend.localhost
> 127.0.0.1  backend.localhost
> ```

### Arrêt

```bash
docker compose -f docker-compose.dev.yml down
```

---

## Endpoints API

| Méthode | Route                     | Description                                      |
|---------|---------------------------|--------------------------------------------------|
| POST    | `/upload`                 | Upload du PDF → `{ session_id, page_count }`    |
| GET     | `/thumbs/{session_id}`    | Liste des URLs de miniatures de la session       |
| GET     | `/thumbs/{session_id}/{page}` | Miniature PNG d'une page spécifique          |
| POST    | `/split`                  | Découpage et téléchargement en zip               |

---

## Structure du projet

```
appli_demo2/
├── backend/
│   ├── main.py              # Point d'entrée FastAPI
│   ├── models.py            # Schémas Pydantic
│   ├── requirements.txt
│   ├── routes/              # upload.py, thumbs.py, split.py
│   └── services/            # pdf_service.py, thumb_service.py,
│                            # crypto_service.py, cleanup.py
├── frontend/
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── src/
│       ├── vite-env.d.ts
│       ├── main.ts
│       ├── App.vue
│       └── components/      # UploadZone.vue, PageGrid.vue,
│                            # PageCard.vue, DownloadButton.vue
├── PRD.md                   # Product Requirements Document
└── ARCHITECTURE.md          # Architecture technique détaillée
```

---

## Sécurité

- Le PDF uploadé est chiffré avec AES-256 sur le serveur
- La clé de déchiffrement n'est jamais écrite sur disque
- Les fichiers temporaires sont supprimés immédiatement après téléchargement
- Nettoyage automatique des sessions de plus de 24h
