## ADDED Requirements

### Requirement: Dépôt de fichier par glisser-déposer
La zone d'upload SHALL accepter le dépôt d'un fichier glissé depuis l'explorateur de fichiers. L'action de dépôt MUST déclencher les mêmes contrôles de validation (type MIME, taille) et le même flux d'upload que la sélection par bouton.

#### Scenario: Dépôt d'un PDF valide
- **WHEN** l'utilisateur glisse un fichier PDF de taille ≤ 10 Mo et le dépose sur la zone d'upload
- **THEN** les validations (type MIME, taille) sont exécutées
- **THEN** l'upload démarre automatiquement vers `POST /upload`

#### Scenario: Dépôt d'un fichier non-PDF
- **WHEN** l'utilisateur dépose un fichier dont le type MIME n'est pas `application/pdf`
- **THEN** un message d'erreur "Le fichier doit être un PDF." est affiché
- **THEN** aucune requête n'est envoyée au serveur

#### Scenario: Dépôt d'un fichier PDF trop volumineux
- **WHEN** l'utilisateur dépose un fichier PDF de taille supérieure à 10 Mo
- **THEN** un message d'erreur "Le fichier ne doit pas dépasser X Mo." est affiché
- **THEN** aucune requête n'est envoyée au serveur

#### Scenario: Dépôt ignoré pendant un upload en cours
- **WHEN** l'utilisateur tente de déposer un fichier alors qu'un upload est déjà en cours
- **THEN** le dépôt est ignoré silencieusement

### Requirement: Retour visuel de la zone de dépôt pendant le survol
La zone d'upload SHALL modifier son apparence visuelle (bordure et fond mis en évidence) lorsqu'un fichier glissé survole la zone, et revenir à son état normal dès que le fichier quitte la zone ou est déposé.

#### Scenario: Entrée d'un fichier glissé dans la zone
- **WHEN** l'utilisateur fait glisser un fichier au-dessus de la zone d'upload
- **THEN** la bordure et le fond de la zone changent visuellement pour indiquer qu'elle est active

#### Scenario: Sortie du fichier glissé hors de la zone
- **WHEN** l'utilisateur fait sortir le fichier glissé hors de la zone d'upload sans déposer
- **THEN** la zone revient à son apparence normale

#### Scenario: Survol des éléments enfants de la zone
- **WHEN** le fichier glissé survole un élément enfant de la zone (icône, texte, bouton)
- **THEN** la zone reste visuellement active sans clignotement
