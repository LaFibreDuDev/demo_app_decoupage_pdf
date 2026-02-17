## Why

L'upload par bouton est fonctionnel mais peu intuitif : le drag & drop est le standard UX attendu pour ce type d'outil (manipulation de fichiers). L'ajouter améliore l'ergonomie sans modifier le flux backend ni introduire de nouvelles dépendances.

## What Changes

- La zone d'upload du frontend (`UploadZone.vue`) devient une zone de dépôt active : l'utilisateur peut y glisser-déposer un fichier PDF directement depuis son explorateur de fichiers.
- Le bouton "Choisir un fichier" reste disponible en complément (les deux modes coexistent).
- La zone de dépôt fournit un retour visuel (highlight) lorsqu'un fichier est survolé (`dragover`).
- Les règles de validation existantes (type MIME, taille ≤ 10 Mo) s'appliquent identiquement aux fichiers déposés.

## Capabilities

### New Capabilities

_(aucune — la fonctionnalité s'intègre dans la capacité existante `pdf-upload`)_

### Modified Capabilities

- `pdf-upload` : ajout du drag & drop comme second mécanisme de sélection de fichier côté frontend. Les requirements existants de validation et d'upload restent inchangés ; de nouveaux requirements couvrent l'interaction drag & drop et le feedback visuel associé.

## Impact

- **Frontend** : `frontend/src/components/UploadZone.vue` — ajout des événements `dragover`, `dragleave`, `drop` et du style de highlight.
- **Backend** : aucun changement (le fichier déposé emprunte le même chemin `POST /upload`).
- **Dépendances** : aucune nouvelle bibliothèque requise (API HTML5 Drag and Drop native).
