## ADDED Requirements

### Requirement: Affichage de la grille de pages après upload
Après un upload réussi, l'interface SHALL afficher une grille de cases numérotées représentant chaque page du PDF. Chaque case MUST afficher le numéro de page centré. Aucune miniature n'est générée pour le MVP.

#### Scenario: Affichage après upload réussi
- **WHEN** l'upload d'un PDF à N pages réussit
- **THEN** une grille de N cases numérotées de 1 à N est affichée sous la zone d'upload

#### Scenario: Grille vide avant upload
- **WHEN** aucun PDF n'a encore été uploadé
- **THEN** aucune grille n'est affichée

### Requirement: Sélection et désélection d'une page
L'interface SHALL permettre à l'utilisateur de sélectionner ou désélectionner une page individuelle en cliquant sur sa case. Une page sélectionnée MUST être visuellement distinguée des pages non sélectionnées (bordure, fond ou indicateur visuel).

#### Scenario: Sélection d'une page
- **WHEN** l'utilisateur clique sur une case non sélectionnée
- **THEN** la case passe à l'état sélectionné avec un indicateur visuel distinct

#### Scenario: Désélection d'une page
- **WHEN** l'utilisateur clique sur une case déjà sélectionnée
- **THEN** la case repasse à l'état non sélectionné

### Requirement: Validation — au moins une page sélectionnée
Le bouton de téléchargement SHALL être désactivé tant qu'aucune page n'est sélectionnée. Il MUST être activé dès qu'au moins une page est cochée.

#### Scenario: Aucune page sélectionnée
- **WHEN** aucune case n'est cochée
- **THEN** le bouton de téléchargement est désactivé et ne peut pas être cliqué

#### Scenario: Au moins une page sélectionnée
- **WHEN** au moins une case est cochée
- **THEN** le bouton de téléchargement est activé

### Requirement: Réinitialisation de la sélection après téléchargement
Après un téléchargement réussi, l'interface SHALL réinitialiser la sélection des pages (toutes décochées) et permettre à l'utilisateur d'uploader un nouveau PDF ou de relancer une sélection.

#### Scenario: Réinitialisation post-téléchargement
- **WHEN** le téléchargement du zip est déclenché avec succès
- **THEN** toutes les cases repassent à l'état non sélectionné
- **THEN** le bouton de téléchargement redevient désactivé
