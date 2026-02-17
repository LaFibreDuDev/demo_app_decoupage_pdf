## 1. Refactorisation de la logique de traitement

- [x] 1.1 Extraire le corps de `onFileSelected()` dans une nouvelle fonction `processFile(file: File)` dans `UploadZone.vue`
- [x] 1.2 Faire retourner `processFile()` immédiatement si `loading.value` est `true`
- [x] 1.3 Adapter `onFileSelected()` pour appeler `processFile(event.target.files[0])`
- [x] 1.4 Vérifier que le comportement existant (sélection via bouton) est inchangé

## 2. Gestion des événements drag & drop

- [x] 2.1 Ajouter les refs `dragCounter` (Number, init 0) et `isDragging` (computed : `dragCounter > 0`) dans `<script setup>`
- [x] 2.2 Ajouter le handler `onDragEnter` : incrémenter `dragCounter`
- [x] 2.3 Ajouter le handler `onDragLeave` : décrémenter `dragCounter`
- [x] 2.4 Ajouter le handler `onDrop(event)` : réinitialiser `dragCounter` à 0, extraire `event.dataTransfer.files[0]`, appeler `processFile()`
- [x] 2.5 Attacher `@dragenter`, `@dragleave`, `@dragover.prevent`, `@drop.prevent` sur le `<div>` conteneur de la zone dans le template

## 3. Retour visuel (highlight)

- [x] 3.1 Remplacer les classes statiques `border-gray-300 bg-white` du conteneur par un binding `:class` conditionnel sur `isDragging`
- [x] 3.2 Appliquer `border-blue-500 bg-blue-50` quand `isDragging` est `true`, `border-gray-300 bg-white` sinon
- [x] 3.3 Mettre à jour le texte indicatif (ex. "Déposez votre PDF ici") affiché uniquement quand `isDragging` est `true`

## 4. Validation et tests manuels

- [x] 4.1 Tester le dépôt d'un PDF valide : l'upload démarre correctement
- [x] 4.2 Tester le dépôt d'un fichier non-PDF : le message d'erreur s'affiche
- [x] 4.3 Tester le dépôt d'un PDF > 10 Mo : le message de taille s'affiche
- [x] 4.4 Tester le glissement sans dépôt : la zone revient à l'état normal
- [x] 4.5 Tester le survol des éléments enfants (icône, bouton) : pas de clignotement du highlight
- [x] 4.6 Tester via MCP Puppeteer : vérifier le rendu visuel et la fonctionnalité drag & drop
