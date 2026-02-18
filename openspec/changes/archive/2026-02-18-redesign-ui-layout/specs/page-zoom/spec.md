## ADDED Requirements

### Requirement: Contrôles de zoom sur la grille de pages
La barre d'outils de la zone principale SHALL proposer deux boutons de zoom (zoom out et zoom in) et un affichage du niveau de zoom courant en pourcentage. Ces contrôles MUST modifier l'affichage de la grille de pages en ajustant le nombre de colonnes.

#### Scenario: Zoom in augmente le nombre de colonnes
- **WHEN** l'utilisateur clique sur le bouton zoom in
- **THEN** le nombre de colonnes de la grille augmente (les cards deviennent plus petites)
- **THEN** le pourcentage affiché augmente d'un cran

#### Scenario: Zoom out diminue le nombre de colonnes
- **WHEN** l'utilisateur clique sur le bouton zoom out
- **THEN** le nombre de colonnes de la grille diminue (les cards deviennent plus grandes)
- **THEN** le pourcentage affiché diminue d'un cran

### Requirement: Limites du zoom
Le zoom SHALL être limité à 5 niveaux discrets (ex. : 60%, 70%, 80%, 90%, 100%, correspondant à 1 à 5 colonnes minimum). Le bouton zoom out MUST être désactivé au niveau minimal. Le bouton zoom in MUST être désactivé au niveau maximal.

#### Scenario: Bouton zoom out désactivé au minimum
- **WHEN** le zoom est au niveau minimal (colonne unique)
- **THEN** le bouton zoom out est désactivé et ne peut pas être cliqué

#### Scenario: Bouton zoom in désactivé au maximum
- **WHEN** le zoom est au niveau maximal (nombre de colonnes maximum)
- **THEN** le bouton zoom in est désactivé et ne peut pas être cliqué

### Requirement: Niveau de zoom par défaut
Le niveau de zoom par défaut SHALL être le niveau intermédiaire (ex. : 80%, soit 3 colonnes), correspondant à l'affichage de référence de la maquette.

#### Scenario: Zoom par défaut à l'ouverture
- **WHEN** l'application est chargée
- **THEN** le niveau de zoom affiché est 80% et la grille affiche 3 colonnes par défaut
