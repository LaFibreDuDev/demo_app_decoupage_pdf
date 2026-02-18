### Requirement: Endpoint GET /thumbs/{session_id} — liste des URLs de miniatures
Le backend SHALL exposer `GET /thumbs/{session_id}` qui retourne un objet JSON `{ "urls": ["…"] }` contenant une URL par page du PDF de la session. Si la session est inconnue ou expirée, il MUST retourner une erreur 404.

#### Scenario: Session valide — premières miniatures demandées
- **WHEN** `GET /thumbs/{session_id}` est appelé pour une session existante dont les miniatures n'ont pas encore été générées
- **THEN** le backend génère toutes les miniatures PNG via pdf2image au DPI configuré
- **THEN** les fichiers sont écrits dans `{TEMP_DIR}/{session_id}/thumbs/page_{n}.png`
- **THEN** le backend retourne `{ "urls": ["/thumbs/{session_id}/1", "/thumbs/{session_id}/2", …] }` avec statut 200

#### Scenario: Session valide — miniatures déjà en cache
- **WHEN** `GET /thumbs/{session_id}` est appelé et les fichiers PNG existent déjà sur disque
- **THEN** le backend retourne directement la liste d'URLs sans regénérer les fichiers

#### Scenario: Session inconnue ou expirée
- **WHEN** `GET /thumbs/{session_id}` est appelé avec un `session_id` dont le répertoire n'existe pas
- **THEN** le backend retourne une erreur 404

### Requirement: Endpoint GET /thumbs/{session_id}/{page} — image PNG d'une page
Le backend SHALL exposer `GET /thumbs/{session_id}/{page}` qui retourne le fichier PNG binaire de la page demandée avec `Content-Type: image/png`. Si la page ou la session est introuvable, il MUST retourner 404.

#### Scenario: Image existante demandée
- **WHEN** `GET /thumbs/{session_id}/{page}` est appelé et le fichier `page_{page}.png` existe en cache
- **THEN** le backend retourne le fichier PNG avec `Content-Type: image/png` et statut 200

#### Scenario: Page hors plage ou session inconnue
- **WHEN** `GET /thumbs/{session_id}/{page}` est appelé avec un numéro de page inexistant ou une session inconnue
- **THEN** le backend retourne une erreur 404

### Requirement: Génération des miniatures via pdf2image au DPI configuré
Le service de génération SHALL utiliser `pdf2image.convert_from_bytes()` avec la résolution définie par `THUMB_DPI` (variable d'environnement). Le PDF MUST être déchiffré en mémoire avant conversion ; aucun fichier PDF en clair ne MUST être écrit sur disque.

#### Scenario: Génération réussie
- **WHEN** le service reçoit les bytes chiffrés d'un PDF valide et la clé de session
- **THEN** les pages sont converties en images PNG à `THUMB_DPI` DPI
- **THEN** chaque image est sauvegardée en `page_{n}.png` dans le dossier `thumbs/` de la session
