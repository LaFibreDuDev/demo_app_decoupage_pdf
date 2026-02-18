## ADDED Requirements

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
