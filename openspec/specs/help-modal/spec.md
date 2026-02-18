### Requirement: Ouverture de la modale d'aide
L'application SHALL afficher une modale d'aide lorsque l'utilisateur clique sur le bouton "Aide" du header. La modale MUST se superposer au contenu existant via un backdrop semi-transparent et être accessible depuis n'importe quel état de l'application (avant ou après upload d'un PDF).

#### Scenario: Ouverture via le bouton Aide
- **WHEN** l'utilisateur clique sur le bouton "Aide" dans le header
- **THEN** la modale d'aide s'affiche par-dessus le contenu avec un backdrop semi-transparent

#### Scenario: Modale accessible avant upload
- **WHEN** aucun PDF n'est chargé et l'utilisateur clique sur "Aide"
- **THEN** la modale s'ouvre normalement

#### Scenario: Modale accessible après upload
- **WHEN** un PDF est chargé et l'utilisateur clique sur "Aide"
- **THEN** la modale s'ouvre sans perturber l'état de la session

### Requirement: Contenu de la modale — tutoriel 3 étapes
La modale SHALL présenter le flux de découpage en 3 étapes numérotées et ordonnées. Chaque étape MUST comporter : un numéro d'ordre, une icône Material Symbols représentative, un titre court et une description explicative.

#### Scenario: Affichage des 3 étapes
- **WHEN** la modale d'aide est ouverte
- **THEN** 3 étapes sont affichées dans l'ordre : (1) Charger un PDF, (2) Sélectionner les pages, (3) Télécharger

#### Scenario: Contenu de l'étape 1
- **WHEN** la modale est ouverte
- **THEN** l'étape 1 affiche l'icône `upload_file`, le titre "Chargez votre PDF" et une description sur le glisser-déposer ou la sélection de fichier

#### Scenario: Contenu de l'étape 2
- **WHEN** la modale est ouverte
- **THEN** l'étape 2 affiche l'icône `touch_app`, le titre "Sélectionnez vos pages" et une description sur le clic pour inclure/exclure des pages

#### Scenario: Contenu de l'étape 3
- **WHEN** la modale est ouverte
- **THEN** l'étape 3 affiche l'icône `download`, le titre "Téléchargez le résultat" et une description sur le choix du mode de sortie et le téléchargement du zip

### Requirement: Fermeture de la modale d'aide
La modale SHALL pouvoir être fermée par trois mécanismes : clic sur le bouton de fermeture (×), clic sur le backdrop, ou appui sur la touche Escape. À la fermeture, le contenu sous-jacent MUST reprendre son état exact sans modification.

#### Scenario: Fermeture via le bouton ×
- **WHEN** la modale est ouverte et l'utilisateur clique sur le bouton ×
- **THEN** la modale se ferme

#### Scenario: Fermeture via le backdrop
- **WHEN** la modale est ouverte et l'utilisateur clique sur le backdrop semi-transparent
- **THEN** la modale se ferme

#### Scenario: Fermeture via Escape
- **WHEN** la modale est ouverte et l'utilisateur appuie sur la touche Escape
- **THEN** la modale se ferme

#### Scenario: État préservé à la fermeture
- **WHEN** la modale est fermée
- **THEN** la session, la sélection de pages et le zoom restent inchangés

### Requirement: Affichage responsive de la modale
La modale SHALL s'adapter à la taille de l'écran. Sur mobile (< 768px), elle MUST occuper toute la largeur de l'écran. Sur desktop, elle MUST être centrée avec une largeur maximale contrainte et un défilement interne si nécessaire.

#### Scenario: Affichage sur mobile
- **WHEN** la modale est ouverte sur un écran < 768px de large
- **THEN** la modale occupe toute la largeur disponible

#### Scenario: Affichage sur desktop
- **WHEN** la modale est ouverte sur un écran ≥ 768px de large
- **THEN** la modale est centrée horizontalement et verticalement avec une largeur maximale
