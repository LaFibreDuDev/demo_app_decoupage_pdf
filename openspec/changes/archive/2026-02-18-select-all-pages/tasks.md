## 1. Frontend — PageGrid.vue

- [x] 1.1 Ajouter la fonction `selectAll()` : assigne `selectedPages.value = Array.from({ length: props.pageCount }, (_, i) => i + 1)`
- [x] 1.2 Ajouter le bouton "Tout sélectionner" dans le template, à gauche de "Tout désélectionner", visible quand `selectedPages.length < pageCount`

## 2. Tests interface

- [x] 2.1 Vérifier avec Puppeteer : le bouton "Tout sélectionner" est visible quand aucune page n'est sélectionnée
- [x] 2.2 Vérifier avec Puppeteer : cliquer "Tout sélectionner" sélectionne toutes les pages et masque le bouton
- [x] 2.3 Vérifier avec Puppeteer : les deux boutons coexistent en sélection partielle
