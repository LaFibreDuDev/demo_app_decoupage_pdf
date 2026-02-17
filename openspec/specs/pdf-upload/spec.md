## ADDED Requirements

### Requirement: Sélection d'un fichier PDF via bouton
L'interface SHALL proposer un bouton permettant à l'utilisateur d'ouvrir le sélecteur de fichiers natif du navigateur, filtré sur les fichiers PDF.

#### Scenario: Ouverture du sélecteur de fichiers
- **WHEN** l'utilisateur clique sur le bouton d'upload
- **THEN** le sélecteur de fichiers du navigateur s'ouvre filtré sur `application/pdf`

### Requirement: Validation côté client du fichier sélectionné
Le frontend SHALL valider le fichier sélectionné avant tout envoi : type MIME `application/pdf` et taille ≤ 10 Mo. En cas d'erreur, un message clair MUST être affiché et l'upload MUST être bloqué.

#### Scenario: Fichier non-PDF sélectionné
- **WHEN** l'utilisateur sélectionne un fichier dont le type n'est pas `application/pdf`
- **THEN** un message d'erreur "Le fichier doit être un PDF." est affiché
- **THEN** aucune requête n'est envoyée au serveur

#### Scenario: Fichier trop volumineux sélectionné
- **WHEN** l'utilisateur sélectionne un fichier PDF de taille supérieure à 10 Mo
- **THEN** un message d'erreur "Le fichier ne doit pas dépasser 10 Mo." est affiché
- **THEN** aucune requête n'est envoyée au serveur

#### Scenario: Fichier PDF valide sélectionné
- **WHEN** l'utilisateur sélectionne un fichier PDF de taille ≤ 10 Mo
- **THEN** l'upload démarre automatiquement vers `POST /upload`

### Requirement: Feedback visuel pendant l'upload
Le frontend SHALL afficher un indicateur de chargement pendant la requête d'upload. Le bouton d'upload MUST être désactivé pendant ce temps.

#### Scenario: Upload en cours
- **WHEN** la requête `POST /upload` est en transit
- **THEN** un indicateur de chargement est visible
- **THEN** le bouton d'upload est désactivé

### Requirement: Réception du résultat d'upload
Après un upload réussi, le frontend SHALL afficher le nombre de pages du PDF et stocker le `session_id` ainsi que le `original_filename` pour les étapes suivantes.

#### Scenario: Upload réussi
- **WHEN** le serveur retourne `{ session_id, page_count, original_filename }` avec statut 200
- **THEN** le message "PDF chargé avec succès — X page(s)" est affiché
- **THEN** le `session_id` est conservé en mémoire dans le composant
- **THEN** le `original_filename` est conservé en mémoire dans le composant

#### Scenario: Erreur serveur à l'upload
- **WHEN** le serveur retourne une erreur (4xx ou 5xx)
- **THEN** le message d'erreur retourné par le serveur est affiché à l'utilisateur

### Requirement: Endpoint POST /upload — réception et validation serveur
Le backend SHALL exposer `POST /upload` acceptant un fichier via `multipart/form-data`. Il MUST valider que le fichier est un PDF valide (magic bytes `%PDF-`) et que sa taille n'excède pas 10 Mo. En cas d'échec, il MUST retourner une erreur HTTP appropriée. En cas de succès, il MUST retourner `{ session_id, page_count, original_filename }`.

#### Scenario: Upload d'un PDF valide
- **WHEN** une requête `POST /upload` est reçue avec un PDF valide ≤ 10 Mo
- **THEN** le serveur retourne `{ session_id: "<uuid>", page_count: <n>, original_filename: "<nom sanitisé>" }` avec statut 200

#### Scenario: Upload d'un fichier non-PDF
- **WHEN** une requête `POST /upload` est reçue avec un fichier dont les magic bytes ne correspondent pas à un PDF
- **THEN** le serveur retourne une erreur 400 avec le message "Fichier invalide : ce n'est pas un PDF."

#### Scenario: Upload d'un fichier trop volumineux
- **WHEN** une requête `POST /upload` est reçue avec un fichier de taille > 10 Mo
- **THEN** le serveur retourne une erreur 413 avec le message "Fichier trop volumineux (max 10 Mo)."

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

### Requirement: Stockage temporaire chiffré du PDF
Le backend SHALL stocker le PDF uploadé chiffré (AES-256) dans un répertoire de session isolé sous `/tmp/pdf_splitter/{session_id}/`. La clé de déchiffrement MUST rester en mémoire uniquement.

#### Scenario: Création du répertoire de session
- **WHEN** un upload réussit
- **THEN** un répertoire `/tmp/pdf_splitter/{session_id}/` est créé
- **THEN** le fichier `original.pdf.enc` y est écrit chiffré

#### Scenario: Clé non stockée sur disque
- **WHEN** un upload réussit
- **THEN** aucun fichier `key.bin` n'existe dans le répertoire de session
- **THEN** la clé AES est uniquement accessible en mémoire du processus
