## Why

L'interface dispose déjà d'un bouton "Tout désélectionner", mais aucun équivalent n'existe pour sélectionner toutes les pages en un clic. Pour les PDFs multi-pages, l'utilisateur doit cliquer manuellement sur chaque page — un bouton "Tout sélectionner" complète la paire et accélère ce cas d'usage fréquent.

## What Changes

- Ajout d'un bouton "Tout sélectionner" dans `PageGrid.vue`, symétrique au bouton "Tout désélectionner" existant.
- Le bouton est visible uniquement lorsqu'au moins une page n'est pas encore sélectionnée (symétrie comportementale avec "Tout désélectionner" qui disparaît quand rien n'est sélectionné).

## Capabilities

### New Capabilities
_(aucune)_

### Modified Capabilities
- `page-selection` : ajout d'un requirement pour la sélection globale de toutes les pages en un clic.

## Impact

- **Frontend** : `PageGrid.vue` uniquement — ajout d'une fonction `selectAll()` et du bouton dans le template.
- **Pas de changement backend ni API.**
