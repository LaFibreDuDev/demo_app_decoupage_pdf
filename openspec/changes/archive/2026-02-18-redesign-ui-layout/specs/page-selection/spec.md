## ADDED Requirements

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
