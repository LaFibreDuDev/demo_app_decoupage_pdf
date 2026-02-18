## MODIFIED Requirements

### Requirement: Header sticky avec logo et actions globales
L'application SHALL afficher un header fixe en haut de page contenant : le logo de l'application (icône ciseau + titre "Découpeur PDF"), un bouton de toggle dark/light mode, et un bouton "Aide". Le header MUST rester visible lors du défilement vertical de la grille de pages. Le bouton "Aide" MUST ouvrir la modale d'aide lors d'un clic.

#### Scenario: Header visible au scroll
- **WHEN** l'utilisateur fait défiler la liste de pages vers le bas
- **THEN** le header reste ancré en haut de la fenêtre et reste visible

#### Scenario: Affichage du logo et du titre
- **WHEN** l'application est chargée
- **THEN** le logo (icône + texte "Découpeur PDF") est visible dans le header

#### Scenario: Clic sur le bouton Aide ouvre la modale
- **WHEN** l'utilisateur clique sur le bouton "Aide" dans le header
- **THEN** la modale d'aide s'affiche
