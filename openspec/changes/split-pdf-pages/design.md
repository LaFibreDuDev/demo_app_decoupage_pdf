## Context

La brique upload est en place : le PDF est stocké chiffré (AES-256) sous `/tmp/pdf_splitter/{session_id}/original.pdf.enc`, la clé vit en mémoire dans `session_keys`. Il faut maintenant permettre à l'utilisateur de sélectionner des pages, d'appeler `POST /split` et de recevoir un zip. Le MVP exclut les miniatures (V1) ; la sélection se fait par numéros de pages uniquement.

## Goals / Non-Goals

**Goals :**
- Endpoint `POST /split` qui déchiffre le PDF de session, extrait les pages choisies avec pikepdf, génère un zip et le streame directement sans écriture disque supplémentaire
- Nommage automatique des fichiers extraits : `originalfilename_pageX.pdf` (page unique) ou `originalfilename_pageX-Y.pdf` (plage)
- Interface de sélection de pages : grille numérotée avec cases à cocher, validation qu'au moins une page est cochée
- Suppression immédiate de la session après envoi du zip
- `UploadResponse` enrichi du champ `original_filename` pour le nommage côté serveur

**Non-Goals :**
- Miniatures PNG des pages (V1)
- Fusion de pages en un seul PDF (V2)
- Sélection par plages textuelles type "1-3, 5" (MVP : cases à cocher individuelles)
- Envoi de plusieurs sélections distinctes dans un seul appel (MVP : une liste de pages → un PDF dans le zip)

## Decisions

### 1. Format du corps de `POST /split`

```json
{
  "session_id": "<uuid>",
  "original_filename": "rapport.pdf",
  "pages": [1, 3, 5]
}
```

**Pages indexées à 1** (côté utilisateur), converties en index 0-based dans le service. Un seul groupe de pages produit un seul PDF dans le zip.

**Alternative écartée :** `selections: [{ pages: [1,3], name: "…" }]` (architecture prévu en V2 pour découpes multiples). Trop complexe pour le MVP — on simplifie à une liste plate de numéros.

### 2. Génération du zip en mémoire

Le zip est construit dans un `io.BytesIO` avec `zipfile.ZipFile` (stdlib), sans écriture disque. La réponse FastAPI utilise `StreamingResponse` avec `media_type="application/zip"`.

**Alternative écartée :** écrire le zip sur disque puis le lire. Inutile pour des fichiers ≤ 10 Mo — la mémoire suffit et évite des fichiers temporaires supplémentaires.

### 3. Déchiffrement en mémoire uniquement

Le PDF est déchiffré via `crypto_service.decrypt_file()` directement dans un `BytesIO`, ouvert par pikepdf sans jamais toucher le disque. Les pages sélectionnées sont écrites dans un second `BytesIO`.

### 4. Nommage automatique des fichiers

- Page unique : `rapport_page3.pdf`
- Plusieurs pages consécutives ou non : `rapport_page1-3-5.pdf` (pages jointes par tirets)
- Le nom de base est déduit de `original_filename` après suppression de l'extension et sanitisation (caractères alphanumériques, tirets, underscores uniquement).

### 5. Suppression de session après envoi

La suppression du répertoire de session (`shutil.rmtree`) et de la clé en mémoire est effectuée dans un `BackgroundTask` FastAPI, **après** la fin du streaming. Cela garantit que les données ne sont pas supprimées avant que le client ait reçu le zip.

### 6. Sélection des pages côté frontend (MVP sans miniatures)

`PageGrid.vue` affiche une grille de cases à cocher numérotées (1 à `page_count`). `PageCard.vue` représente une case individuelle. Pas de miniature pour le MVP — juste le numéro centré sur fond gris. `DownloadButton.vue` est désactivé tant qu'aucune page n'est sélectionnée.

### 7. Transmission du `original_filename`

`UploadResponse` gagne un champ `original_filename: str` (nom sanitisé sans chemin). Le frontend le stocke dans l'état d'`App.vue` et le transmet dans le corps de `POST /split`. Cela évite de stocker le nom sur disque côté serveur.

## Risks / Trade-offs

- **Perte de session si le serveur redémarre** → la clé AES est en mémoire ; un redémarrage invalide toutes les sessions en cours. Acceptable pour le MVP (fichiers ≤ 10 Mo, usage court).
- **Zip en mémoire pour fichiers volumineux** → pour le MVP (≤ 10 Mo), le pic mémoire reste raisonnable (PDF original + pages extraites + zip ≈ 2× la taille du PDF). Pas un problème à cette échelle.
- **Suppression en BackgroundTask** → si le processus est tué pendant le streaming, la session peut ne pas être supprimée. Le cleanup automatique des sessions > 24h (futur `cleanup.py`) est le filet de sécurité.
