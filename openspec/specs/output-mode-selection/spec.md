## ADDED Requirements

### Requirement: Sélecteur de mode de sortie dans l'interface
Le frontend SHALL afficher un sélecteur de mode de sortie permettant à l'utilisateur de choisir entre `merged` (toutes les pages sélectionnées fusionnées dans un seul PDF) et `separate` (un PDF par page dans le zip). Le mode par défaut MUST être `merged`. Le sélecteur MUST être visible avant le déclenchement du téléchargement.

#### Scenario: Affichage du sélecteur
- **WHEN** l'interface est dans l'état "PDF chargé"
- **THEN** un sélecteur de mode (deux options : "Fichier fusionné" et "Un fichier par page") est affiché au-dessus du bouton de téléchargement
- **THEN** l'option "Fichier fusionné" est sélectionnée par défaut

#### Scenario: Sélection du mode "séparé"
- **WHEN** l'utilisateur sélectionne l'option "Un fichier par page"
- **THEN** le mode actif passe à `separate`
- **THEN** le libellé du bouton de téléchargement reflète le mode choisi

#### Scenario: Sélection du mode "fusionné"
- **WHEN** l'utilisateur sélectionne l'option "Fichier fusionné"
- **THEN** le mode actif passe à `merged`

#### Scenario: Transmission du mode au backend
- **WHEN** l'utilisateur clique sur le bouton de téléchargement
- **THEN** la requête `POST /split` inclut le champ `output_mode` avec la valeur correspondant au mode sélectionné

#### Scenario: Réinitialisation après téléchargement
- **WHEN** le téléchargement se termine avec succès
- **THEN** le mode de sortie est réinitialisé à `merged`
