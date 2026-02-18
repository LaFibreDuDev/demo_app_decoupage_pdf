## MODIFIED Requirements

### Requirement: Affichage de la grille de pages après upload
Après un upload réussi, l'interface SHALL afficher une grille de cartes représentant chaque page du PDF. Chaque carte MUST afficher la miniature PNG de la page récupérée depuis `GET /thumbs/{session_id}`, avec le numéro de page visible en overlay. Pendant le chargement des miniatures, chaque carte MUST afficher un skeleton animé (animation pulse) couvrant la zone image, avec le numéro de page visible en overlay sur le skeleton.

#### Scenario: Affichage après upload réussi
- **WHEN** l'upload d'un PDF à N pages réussit
- **THEN** une grille de N cartes numérotées de 1 à N est affichée sous la zone d'upload
- **THEN** `GET /thumbs/{session_id}` est appelé pour récupérer les URLs de miniatures

#### Scenario: Miniatures chargées avec succès
- **WHEN** `GET /thumbs/{session_id}` retourne la liste d'URLs
- **THEN** chaque carte affiche la miniature PNG correspondant à sa page
- **THEN** le numéro de page reste visible en overlay sur la miniature

#### Scenario: Chargement des miniatures en cours
- **WHEN** la requête `GET /thumbs/{session_id}` est en transit
- **THEN** chaque carte affiche un skeleton animé (animate-pulse) couvrant la zone image
- **THEN** le numéro de page est visible en overlay sur le skeleton
- **THEN** le skeleton respecte le ratio portrait de la carte (aspect-[3/4])
- **THEN** le skeleton adapte sa couleur au thème actif (clair : bg-slate-200, sombre : bg-slate-700)

#### Scenario: Grille vide avant upload
- **WHEN** aucun PDF n'a encore été uploadé
- **THEN** aucune grille n'est affichée
