## ADDED Requirements

### Requirement: Endpoint POST /split — réception et validation
Le backend SHALL exposer `POST /split` acceptant un corps JSON `{ session_id, original_filename, pages }`. Il MUST vérifier que la session existe en mémoire (clé AES présente) et que la liste `pages` est non vide. En cas d'échec, il MUST retourner une erreur HTTP appropriée.

#### Scenario: Requête valide
- **WHEN** une requête `POST /split` est reçue avec un `session_id` valide et une liste `pages` non vide
- **THEN** le serveur traite la requête et retourne un zip avec statut 200

#### Scenario: Session inconnue
- **WHEN** une requête `POST /split` est reçue avec un `session_id` absent du dictionnaire de clés en mémoire
- **THEN** le serveur retourne une erreur 404 avec le message "Session introuvable ou expirée."

#### Scenario: Liste de pages vide
- **WHEN** une requête `POST /split` est reçue avec `pages: []`
- **THEN** le serveur retourne une erreur 400 avec le message "Aucune page sélectionnée."

#### Scenario: Numéro de page hors limites
- **WHEN** une requête `POST /split` contient un numéro de page supérieur au nombre de pages du PDF
- **THEN** le serveur retourne une erreur 400 avec le message "Numéro de page invalide."

### Requirement: Découpage du PDF et génération du zip en mémoire
Le backend SHALL déchiffrer le PDF de session en mémoire, extraire les pages demandées avec pikepdf, générer un zip en mémoire (sans écriture disque) et le retourner via `StreamingResponse`. Le zip MUST contenir un unique fichier PDF avec les pages extraites dans l'ordre fourni.

#### Scenario: Zip retourné en streaming
- **WHEN** la requête est valide
- **THEN** la réponse a le `Content-Type: application/zip`
- **THEN** le `Content-Disposition` indique un nom de fichier en `.zip`
- **THEN** le zip contient un fichier PDF avec exactement les pages demandées

### Requirement: Nommage automatique des fichiers extraits
Le backend SHALL nommer le fichier PDF extrait selon le pattern `{basename}_page{X}.pdf` pour une page unique ou `{basename}_page{X}-{Y}-…pdf` pour plusieurs pages. Le `basename` MUST être le nom du fichier original sans extension, sanitisé (caractères alphanumériques, tirets et underscores uniquement).

#### Scenario: Page unique extraite
- **WHEN** `pages: [3]` et `original_filename: "rapport annuel.pdf"`
- **THEN** le fichier dans le zip se nomme `rapport_annuel_page3.pdf`

#### Scenario: Plusieurs pages extraites
- **WHEN** `pages: [1, 3, 5]` et `original_filename: "doc.pdf"`
- **THEN** le fichier dans le zip se nomme `doc_page1-3-5.pdf`

### Requirement: Suppression de la session après envoi du zip
Le backend SHALL supprimer le répertoire de session et la clé AES en mémoire immédiatement après la fin du streaming du zip, via un `BackgroundTask`. Aucun fichier temporaire de la session ne MUST subsister sur disque après la complétion du téléchargement.

#### Scenario: Suppression post-streaming
- **WHEN** le streaming du zip est terminé
- **THEN** le répertoire `/tmp/pdf_splitter/{session_id}/` n'existe plus
- **THEN** la clé AES correspondante est retirée du dictionnaire en mémoire

### Requirement: Déclenchement du téléchargement depuis le frontend
Le frontend SHALL envoyer `POST /api/split` avec `{ session_id, original_filename, pages }` au clic sur le bouton de téléchargement, initier le téléchargement du zip via un lien temporaire (`URL.createObjectURL`), et afficher un indicateur de chargement pendant la requête. Le bouton MUST être désactivé pendant ce temps.

#### Scenario: Téléchargement initié
- **WHEN** l'utilisateur clique sur le bouton de téléchargement avec au moins une page sélectionnée
- **THEN** une requête `POST /api/split` est envoyée
- **THEN** le bouton est désactivé et un indicateur de chargement est affiché

#### Scenario: Téléchargement réussi
- **WHEN** le serveur retourne le zip avec statut 200
- **THEN** le navigateur propose le téléchargement du fichier zip
- **THEN** la sélection des pages est réinitialisée

#### Scenario: Erreur lors du split
- **WHEN** le serveur retourne une erreur (4xx ou 5xx)
- **THEN** le message d'erreur est affiché à l'utilisateur
- **THEN** le bouton redevient actif
