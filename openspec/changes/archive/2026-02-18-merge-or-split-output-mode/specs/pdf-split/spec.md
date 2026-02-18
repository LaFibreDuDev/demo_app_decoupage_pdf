## MODIFIED Requirements

### Requirement: Endpoint POST /split — réception et validation
Le backend SHALL exposer `POST /split` acceptant un corps JSON `{ session_id, original_filename, pages, output_mode? }`. Le champ `output_mode` est optionnel et MUST valoir `"merged"` ou `"separate"` ; sa valeur par défaut MUST être `"merged"`. Il MUST vérifier que la session existe en mémoire (clé AES présente) et que la liste `pages` est non vide. En cas d'échec, il MUST retourner une erreur HTTP appropriée.

#### Scenario: Requête valide sans output_mode
- **WHEN** une requête `POST /split` est reçue avec un `session_id` valide, une liste `pages` non vide et sans champ `output_mode`
- **THEN** le serveur traite la requête en mode `merged` et retourne un zip avec statut 200

#### Scenario: Requête valide avec output_mode "separate"
- **WHEN** une requête `POST /split` est reçue avec `output_mode: "separate"`
- **THEN** le serveur traite la requête en mode `separate` et retourne un zip avec statut 200

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
Le backend SHALL déchiffrer le PDF de session en mémoire, extraire les pages demandées avec pikepdf, générer un zip en mémoire (sans écriture disque) et le retourner via `StreamingResponse`. Le contenu du zip MUST dépendre du mode de sortie : en mode `merged`, le zip contient un unique fichier PDF avec toutes les pages extraites dans l'ordre fourni ; en mode `separate`, le zip contient un fichier PDF distinct par page sélectionnée.

#### Scenario: Zip en mode "merged"
- **WHEN** la requête est valide avec `output_mode: "merged"` (ou sans `output_mode`)
- **THEN** la réponse a le `Content-Type: application/zip`
- **THEN** le zip contient exactement un fichier PDF regroupant toutes les pages demandées

#### Scenario: Zip en mode "separate"
- **WHEN** la requête est valide avec `output_mode: "separate"` et `pages: [1, 3, 5]`
- **THEN** la réponse a le `Content-Type: application/zip`
- **THEN** le zip contient exactement 3 fichiers PDF, un par page sélectionnée

### Requirement: Nommage automatique des fichiers extraits
Le backend SHALL nommer les fichiers PDF extraits selon le mode de sortie. En mode `merged` : `{basename}_page{X}-{Y}-….pdf` (pages jointes par `-`). En mode `separate` : chaque fichier est nommé `{basename}_page{N}.pdf` où `N` est le numéro de la page. Le `basename` MUST être le nom du fichier original sans extension, sanitisé (caractères alphanumériques, tirets et underscores uniquement).

#### Scenario: Mode "merged" — page unique
- **WHEN** `pages: [3]`, `output_mode: "merged"` et `original_filename: "rapport annuel"`
- **THEN** le fichier dans le zip se nomme `rapport_annuel_page3.pdf`

#### Scenario: Mode "merged" — plusieurs pages
- **WHEN** `pages: [1, 3, 5]`, `output_mode: "merged"` et `original_filename: "doc"`
- **THEN** le fichier dans le zip se nomme `doc_page1-3-5.pdf`

#### Scenario: Mode "separate" — plusieurs pages
- **WHEN** `pages: [1, 3, 5]`, `output_mode: "separate"` et `original_filename: "doc"`
- **THEN** le zip contient `doc_page1.pdf`, `doc_page3.pdf` et `doc_page5.pdf`

### Requirement: Déclenchement du téléchargement depuis le frontend
Le frontend SHALL envoyer `POST /api/split` avec `{ session_id, original_filename, pages, output_mode }` au clic sur le bouton de téléchargement, initier le téléchargement du zip via un lien temporaire (`URL.createObjectURL`), et afficher un indicateur de chargement pendant la requête. Le bouton MUST être désactivé pendant ce temps.

#### Scenario: Téléchargement initié
- **WHEN** l'utilisateur clique sur le bouton de téléchargement avec au moins une page sélectionnée
- **THEN** une requête `POST /api/split` est envoyée avec le champ `output_mode` correspondant au mode sélectionné
- **THEN** le bouton est désactivé et un indicateur de chargement est affiché

#### Scenario: Téléchargement réussi
- **WHEN** le serveur retourne le zip avec statut 200
- **THEN** le navigateur propose le téléchargement du fichier zip
- **THEN** la sélection des pages est réinitialisée

#### Scenario: Erreur lors du split
- **WHEN** le serveur retourne une erreur (4xx ou 5xx)
- **THEN** le message d'erreur est affiché à l'utilisateur
- **THEN** le bouton redevient actif
