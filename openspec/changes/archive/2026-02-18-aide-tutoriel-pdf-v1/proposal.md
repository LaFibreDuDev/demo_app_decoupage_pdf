## Why

L'application ne fournit aucune aide contextuelle : un nouvel utilisateur ne sait pas dans quel ordre effectuer les actions (charger → sélectionner → télécharger), ni ce que signifient les options disponibles. Un texte d'aide ou un tutoriel pas-à-pas guidé réduirait le taux d'abandon et les erreurs d'utilisation dès la V1.

## What Changes

- Ajout d'un panneau d'aide modale accessible via le bouton "Aide" déjà présent dans l'en-tête.
- Le panneau explique le flux complet en 3 étapes : charger un PDF, sélectionner les pages, télécharger le découpage.
- Chaque étape inclut une courte description et une icône cohérente avec le reste de l'interface (Material Symbols).
- Aucune modification des routes backend ni des composants existants (ajout pur).

## Capabilities

### New Capabilities
- `help-modal`: Panneau d'aide modale présentant le tutoriel en 3 étapes du processus de découpage PDF.

### Modified Capabilities
- `ui-layout`: Le bouton "Aide" de l'AppHeader doit désormais ouvrir la modale au lieu d'être inerte.

## Impact

- Nouveau composant `HelpModal.vue` dans `frontend/src/components/`.
- `AppHeader.vue` : le bouton "Aide" émet un événement `open-help`.
- `App.vue` : gestion de l'état `helpOpen` et câblage de l'événement.
- Aucun impact backend, aucune nouvelle dépendance.
