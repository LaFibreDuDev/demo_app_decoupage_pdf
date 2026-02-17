## MODIFIED Requirements

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
