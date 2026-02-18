## Why

L'interface actuelle de l'application manque de structure visuelle et d'ergonomie : les contrôles sont dispersés, il n'y a pas de hiérarchie claire entre la configuration et la grille de pages, et l'expérience utilisateur est peu soignée. Un maquettage de référence a été produit (`docs/design/`) et doit servir de cible pour aligner l'application sur un niveau de qualité production.

## What Changes

- **BREAKING** Refonte du layout : abandon du layout en colonne unique au profit d'un layout sidebar + zone principale (deux colonnes)
- Ajout d'un header sticky avec logo, titre et boutons d'action (mode sombre, aide)
- Déplacement des contrôles de configuration (mode de sortie), sélection rapide et bouton de téléchargement dans la sidebar gauche
- Ajout d'une barre d'outils dans la zone principale (nom du fichier, nombre de pages, contrôles de zoom)
- Refonte des cards de pages : état sélectionné (bordure bleue, ring, checkmark, badge numéro bleu, label "Inclus") vs état non sélectionné (grayscale, opacity réduite, overlay "+" au survol)
- Ajout d'un toast de notification bas de page pour les événements système (upload réussi, erreurs)
- Ajout du support du mode sombre (toggle header)
- Ajout de boutons de sélection rapide : "Pages paires", "Pages impaires", "Réinitialiser"
- Ajout de contrôles de zoom sur la grille de pages
- Intégration de la police Inter et des icônes Material Symbols Outlined

## Capabilities

### New Capabilities
- `ui-layout`: Layout principal de l'application — header sticky, sidebar gauche, zone principale avec barre d'outils et grille de pages
- `dark-mode`: Support du mode sombre avec toggle dans le header, persistant via classe CSS sur `<html>`
- `page-zoom`: Contrôles de zoom (zoom in / zoom out / affichage du pourcentage) sur la grille de pages
- `upload-toast`: Notification toast fixe en bas de page lors d'un upload réussi (ou erreur), avec bouton de fermeture

### Modified Capabilities
- `page-selection`: Ajout de raccourcis de sélection rapide — "Pages paires", "Pages impaires", "Réinitialiser" — en complément de la sélection individuelle existante

## Impact

- **Frontend** : refonte complète de `App.vue` et des composants `UploadZone.vue`, `PageGrid.vue`, `PageCard.vue`, `DownloadButton.vue` ; nouveaux composants `AppHeader.vue`, `AppSidebar.vue`, `PageToolbar.vue`, `UploadToast.vue`
- **Styles** : ajout de la police Inter (Google Fonts) et Material Symbols Outlined ; configuration Tailwind étendue (couleur `primary`, `background-light/dark`, `fontFamily.display`)
- **Aucun impact backend** : changement purement frontend
- **Dépendances** : aucune nouvelle bibliothèque JS — uniquement CDN Google Fonts (déjà présent dans le prototype de référence)
