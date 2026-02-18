## ADDED Requirements

### Requirement: Header sticky avec logo et actions globales
L'application SHALL afficher un header fixe en haut de page contenant : le logo de l'application (icône ciseau + titre "Découpeur PDF"), un bouton de toggle dark/light mode, et un bouton "Aide". Le header MUST rester visible lors du défilement vertical de la grille de pages.

#### Scenario: Header visible au scroll
- **WHEN** l'utilisateur fait défiler la liste de pages vers le bas
- **THEN** le header reste ancré en haut de la fenêtre et reste visible

#### Scenario: Affichage du logo et du titre
- **WHEN** l'application est chargée
- **THEN** le logo (icône + texte "Découpeur PDF") est visible dans le header

### Requirement: Layout sidebar + zone principale
L'interface principale SHALL utiliser un layout deux colonnes : une sidebar gauche fixe et une zone principale scrollable. La sidebar MUST avoir une largeur fixe (320px) et ne doit pas défiler avec le contenu de la grille. La zone principale MUST occuper l'espace restant.

#### Scenario: Affichage du layout deux colonnes
- **WHEN** l'application est chargée
- **THEN** la sidebar est visible à gauche et la zone principale occupe le reste de l'écran

#### Scenario: Sidebar fixe pendant le scroll de la grille
- **WHEN** l'utilisateur fait défiler la grille de pages
- **THEN** la sidebar ne défile pas et reste visible dans son intégralité

### Requirement: Sidebar — section Configuration du mode de sortie
La sidebar SHALL contenir une section "Configuration" permettant de choisir le mode de sortie via deux boutons radio : "Fichier fusionné" (toutes les pages dans un seul PDF) et "Fichiers individuels" (un PDF par page). L'option sélectionnée MUST être visuellement mise en évidence (bordure colorée, fond teinté).

#### Scenario: Mode fusionné sélectionné par défaut
- **WHEN** l'application est chargée
- **THEN** l'option "Fichier fusionné" est sélectionnée par défaut

#### Scenario: Changement de mode de sortie
- **WHEN** l'utilisateur clique sur une option radio non sélectionnée
- **THEN** cette option devient active et l'autre est désactivée

### Requirement: Sidebar — section Sélection rapide
La sidebar SHALL contenir une section "Sélection" avec des boutons de sélection rapide : "Tout sélectionner", "Pages paires", "Pages impaires", "Réinitialiser". Ces boutons MUST être fonctionnels uniquement lorsqu'un PDF est chargé.

#### Scenario: Boutons visibles après upload
- **WHEN** un PDF a été uploadé avec succès
- **THEN** les boutons "Pages paires", "Pages impaires" et "Réinitialiser" sont affichés dans la section Sélection

### Requirement: Sidebar — section Sécurité et Confidentialité
La sidebar SHALL afficher une section "Sécurité & Confidentialité" listant deux indicateurs : "Fichiers chiffrés sur le serveur" (icône cadenas) et "Suppression automatique après 24h" (icône historique).

#### Scenario: Indicateurs de sécurité toujours visibles
- **WHEN** l'application est chargée
- **THEN** les deux indicateurs de sécurité sont affichés dans la sidebar

### Requirement: Sidebar — résumé et bouton de téléchargement
En bas de la sidebar, l'interface SHALL afficher un résumé de la sélection courante (nombre de pages sélectionnées) et un bouton de téléchargement prominent. Le bouton MUST être désactivé si aucune page n'est sélectionnée.

#### Scenario: Résumé mis à jour dynamiquement
- **WHEN** l'utilisateur sélectionne ou désélectionne des pages
- **THEN** le compteur "Sélectionné : N pages" dans la sidebar reflète le nombre courant

#### Scenario: Bouton de téléchargement désactivé sans sélection
- **WHEN** aucune page n'est sélectionnée
- **THEN** le bouton de téléchargement est désactivé

### Requirement: Zone principale — barre d'outils du document
La zone principale SHALL afficher une barre d'outils au-dessus de la grille contenant : l'icône document + le nom du fichier chargé + un badge indiquant le nombre de pages. Les contrôles de zoom (boutons +/- et affichage du pourcentage) MUST également être présents dans cette barre.

#### Scenario: Affichage du nom de fichier
- **WHEN** un PDF a été uploadé
- **THEN** le nom du fichier est affiché dans la barre d'outils de la zone principale

#### Scenario: Badge du nombre de pages
- **WHEN** un PDF a été uploadé
- **THEN** le nombre total de pages est affiché sous forme de badge dans la barre d'outils

### Requirement: Zone principale — état initial avant upload
Avant qu'un PDF soit uploadé, la zone principale SHALL afficher la zone de dépôt de fichier (drag-and-drop) centrée, permettant à l'utilisateur de sélectionner son fichier.

#### Scenario: Zone d'upload visible avant tout upload
- **WHEN** l'application est chargée et aucun PDF n'a encore été uploadé
- **THEN** la zone de dépôt de fichier est affichée dans la zone principale

#### Scenario: Zone d'upload masquée après upload
- **WHEN** un PDF a été uploadé avec succès
- **THEN** la zone de dépôt est remplacée par la grille de pages
