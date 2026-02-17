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
| Frontend    | Vue 3 + Vite + Tailwind CSS v3  |
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

### 2. Frontend (Vue 3 + Vite)

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

## Endpoints API

| Méthode | Route                     | Description                                      |
|---------|---------------------------|--------------------------------------------------|
| POST    | `/upload`                 | Upload du PDF → `{ session_id, page_count }`    |
| GET     | `/thumbs/{session_id}`    | Miniatures PNG de chaque page                    |
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
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── src/
│       ├── main.js
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
