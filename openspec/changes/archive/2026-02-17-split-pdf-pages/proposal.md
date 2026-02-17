## Why

La première brique du MVP permet d'uploader et de stocker un PDF chiffré en session. Il faut maintenant permettre à l'utilisateur de sélectionner les pages à extraire, de déclencher le découpage côté serveur et de télécharger le résultat en zip — ce qui constitue la finalité principale de l'application.

## What Changes

- Ajout d'une interface de sélection des pages dans le frontend (grille de cases à cocher numérotées, sans miniatures pour le MVP)
- Ajout de l'endpoint `POST /split` côté backend : reçoit `session_id` et la liste des pages sélectionnées, découpe le PDF avec pikepdf, génère un zip en mémoire et le retourne en streaming
- Ajout d'un bouton de téléchargement dans le frontend qui déclenche l'appel `/split` et initie le téléchargement du zip
- Suppression immédiate des fichiers temporaires de session après l'envoi du zip
- Enregistrement de la route `/split` dans `main.py`

## Capabilities

### New Capabilities

- `page-selection` : sélection des pages à extraire dans le frontend — grille de numéros de page avec cases à cocher, validation qu'au moins une page est sélectionnée avant de permettre le téléchargement
- `pdf-split` : endpoint `POST /split` backend — déchiffrement du PDF de session, découpage des pages sélectionnées avec pikepdf, nommage automatique (`originalfilename_pageX-Y.pdf`), création d'un zip en mémoire, streaming de la réponse, suppression immédiate des fichiers temporaires

### Modified Capabilities

- `pdf-upload` : le composant `UploadZone.vue` doit émettre le nom du fichier original en plus de `session_id` et `page_count`, afin que le backend puisse nommer correctement les fichiers découpés

## Impact

- **Backend** : nouveau fichier `routes/split.py`, nouveau fichier `services/pdf_service.py` (fonction de découpage), mise à jour `main.py` pour inclure la route split, modèle Pydantic `SplitRequest` dans `models.py`
- **Frontend** : nouveau composant `PageGrid.vue`, nouveau composant `PageCard.vue`, nouveau composant `DownloadButton.vue`, mise à jour `App.vue` pour orchestrer la sélection et le téléchargement
- **Modèle** : `UploadResponse` enrichi du champ `original_filename`
- **Dépendances** : pas de nouvelle bibliothèque — pikepdf et zipfile (stdlib) suffisent
