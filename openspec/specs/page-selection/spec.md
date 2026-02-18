## ADDED Requirements

### Requirement: Affichage de la grille de pages après upload
Après un upload réussi, l'interface SHALL afficher une grille de cartes représentant chaque page du PDF. Chaque carte MUST afficher la miniature PNG de la page récupérée depuis `GET /thumbs/{session_id}`, avec le numéro de page visible en overlay. Pendant le chargement des miniatures, chaque carte MUST afficher le numéro de page centré comme état intermédiaire.

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
- **THEN** chaque carte affiche le numéro de page centré en attendant

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

### Requirement: Sélection globale de toutes les pages
L'interface SHALL afficher un bouton "Tout sélectionner" permettant de sélectionner toutes les pages du PDF en un clic. Ce bouton MUST être visible uniquement lorsqu'au moins une page n'est pas encore sélectionnée. Il MUST être placé à gauche du bouton "Tout désélectionner" existant.

#### Scenario: Affichage quand aucune page n'est sélectionnée
- **WHEN** aucune page n'est sélectionnée
- **THEN** le bouton "Tout sélectionner" est affiché

#### Scenario: Affichage quand une partie des pages est sélectionnée
- **WHEN** au moins une page est sélectionnée et au moins une ne l'est pas
- **THEN** les boutons "Tout sélectionner" et "Tout désélectionner" sont tous deux affichés

#### Scenario: Masquage quand toutes les pages sont sélectionnées
- **WHEN** toutes les pages du PDF sont sélectionnées
- **THEN** le bouton "Tout sélectionner" est masqué
- **THEN** le bouton "Tout désélectionner" est affiché

#### Scenario: Clic sur "Tout sélectionner"
- **WHEN** l'utilisateur clique sur le bouton "Tout sélectionner"
- **THEN** toutes les pages du PDF passent à l'état sélectionné
- **THEN** le compteur de pages sélectionnées reflète le nombre total de pages

### Requirement: Réinitialisation de la sélection après téléchargement
Après un téléchargement réussi, l'interface SHALL réinitialiser la sélection des pages (toutes décochées) et permettre à l'utilisateur d'uploader un nouveau PDF ou de relancer une sélection.

#### Scenario: Réinitialisation post-téléchargement
- **WHEN** le téléchargement du zip est déclenché avec succès
- **THEN** toutes les cases repassent à l'état non sélectionné
- **THEN** le bouton de téléchargement redevient désactivé

### Requirement: Sélection rapide des pages paires
La sidebar SHALL proposer un bouton "Pages paires" qui sélectionne en un clic toutes les pages ayant un numéro pair (2, 4, 6…) parmi les pages du PDF chargé. Cette sélection MUST remplacer la sélection courante.

#### Scenario: Clic sur "Pages paires"
- **WHEN** l'utilisateur clique sur le bouton "Pages paires"
- **THEN** seules les pages ayant un numéro pair sont sélectionnées
- **THEN** toute sélection précédente est remplacée

#### Scenario: PDF avec une seule page impaire
- **WHEN** le PDF ne contient que des pages impaires (ex. : 1 seule page)
- **THEN** cliquer "Pages paires" ne sélectionne aucune page

### Requirement: Sélection rapide des pages impaires
La sidebar SHALL proposer un bouton "Pages impaires" qui sélectionne en un clic toutes les pages ayant un numéro impair (1, 3, 5…) parmi les pages du PDF chargé. Cette sélection MUST remplacer la sélection courante.

#### Scenario: Clic sur "Pages impaires"
- **WHEN** l'utilisateur clique sur le bouton "Pages impaires"
- **THEN** seules les pages ayant un numéro impair sont sélectionnées
- **THEN** toute sélection précédente est remplacée

### Requirement: Réinitialisation de la sélection via la sidebar
La sidebar SHALL proposer un bouton "Réinitialiser" qui désélectionne toutes les pages en un clic.

#### Scenario: Clic sur "Réinitialiser"
- **WHEN** l'utilisateur clique sur le bouton "Réinitialiser"
- **THEN** toutes les pages sont désélectionnées
- **THEN** le compteur de sélection revient à 0

#### Scenario: Réinitialisation sans sélection active
- **WHEN** aucune page n'est sélectionnée et l'utilisateur clique sur "Réinitialiser"
- **THEN** aucun changement n'est visible (état déjà vide)
