### Requirement: Toast de confirmation après upload réussi
Après un upload PDF réussi, l'interface SHALL afficher un toast de notification en position fixe en bas de la fenêtre. Ce toast MUST indiquer que le document a été chargé avec succès, et afficher le nom du fichier et sa taille. Un bouton de fermeture MUST être présent.

#### Scenario: Affichage après upload réussi
- **WHEN** l'upload d'un PDF se termine avec succès
- **THEN** un toast apparaît en bas de la page avec une icône de succès (vert), le nom du fichier et sa taille

#### Scenario: Bouton de fermeture du toast
- **WHEN** l'utilisateur clique sur le bouton de fermeture du toast
- **THEN** le toast disparaît immédiatement

### Requirement: Auto-fermeture du toast
Le toast SHALL se fermer automatiquement après 5 secondes sans intervention de l'utilisateur.

#### Scenario: Fermeture automatique après délai
- **WHEN** le toast est affiché et que 5 secondes s'écoulent sans interaction
- **THEN** le toast disparaît automatiquement

#### Scenario: Le toast ne se rouvre pas seul
- **WHEN** le toast a été fermé (manuellement ou automatiquement)
- **THEN** il ne réapparaît pas sauf si un nouvel upload est effectué

### Requirement: Affichage de la taille du fichier
Le toast SHALL afficher la taille du fichier uploadé en mégaoctets (Mo) avec une décimale, tel que retourné par le backend dans la réponse d'upload.

#### Scenario: Taille affichée en Mo
- **WHEN** le toast est affiché après un upload
- **THEN** la taille du fichier est indiquée au format "X.X Mo"
