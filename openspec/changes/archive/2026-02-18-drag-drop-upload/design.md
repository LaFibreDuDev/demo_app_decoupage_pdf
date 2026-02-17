## Context

`UploadZone.vue` expose actuellement un seul point d'entrée : un bouton qui ouvre le sélecteur de fichiers natif. La validation et l'upload sont encapsulés dans `onFileSelected()`. L'objectif est d'ajouter le drag & drop sans dupliquer cette logique et sans toucher au backend.

## Goals / Non-Goals

**Goals:**
- Permettre le dépôt d'un fichier PDF par glisser-déposer sur la zone d'upload.
- Afficher un highlight visuel (bordure + fond) pendant le survol d'un fichier glissé.
- Réutiliser la logique de validation et d'envoi existante pour les fichiers déposés.

**Non-Goals:**
- Support du dépôt de plusieurs fichiers simultanément.
- Dépôt depuis une autre onglet/application web (hors fichiers système).
- Modifications côté backend.

## Decisions

### 1. Extraire la logique de traitement dans `processFile(file)`

**Décision** : refactoriser `onFileSelected()` pour déléguer validation + upload à une fonction `processFile(file: File)`. Les deux handlers (`onFileSelected` et `onDrop`) l'appellent avec le fichier obtenu de leur source respective.

**Pourquoi** : évite la duplication de la logique de validation et d'upload. Alternative rejetée : copier-coller le bloc dans `onDrop` — fragile à la maintenance.

---

### 2. Attacher les événements drag sur le conteneur extérieur

**Décision** : les événements `@dragenter`, `@dragleave`, `@dragover.prevent`, `@drop.prevent` sont posés sur le `<div>` dashed border qui enveloppe déjà toute la zone.

**Pourquoi** : c'est la surface visible que l'utilisateur vise. Alternative rejetée : un overlay absolu dédié — complexité inutile pour un seul composant.

---

### 3. Compteur `dragCounter` pour le highlight

**Décision** : utiliser un `ref` entier `dragCounter` incrémenté sur `dragenter` et décrémenté sur `dragleave`. `isDragging` est `true` quand `dragCounter > 0`.

**Pourquoi** : l'événement `dragleave` se déclenche en entrant dans un enfant du conteneur (SVG, bouton…), ce qui ferait clignoter le highlight sans ce compteur. Alternative rejetée : vérifier `event.relatedTarget` — fiabilité cross-browser inégale.

---

### 4. Binding de classe conditionnel pour le highlight

**Décision** : utiliser `:class` sur le conteneur pour alterner entre les classes Tailwind `border-gray-300 bg-white` (repos) et `border-blue-500 bg-blue-50` (survol actif).

**Pourquoi** : cohérent avec l'utilisation de Tailwind existante dans le composant, sans CSS additionnel.

## Risks / Trade-offs

- **Dragleave sur les enfants** → résolu par le compteur `dragCounter` (voir Décision 3).
- **Fichier non-PDF déposé** → la validation existante dans `processFile()` affiche le message d'erreur approprié ; aucun traitement spécifique au drop nécessaire.
- **Désactivation pendant le chargement** : si `loading` est `true`, le drop doit être ignoré pour éviter un double envoi. `processFile()` peut retourner immédiatement si `loading.value` est vrai.
