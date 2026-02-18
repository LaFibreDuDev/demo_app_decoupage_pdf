## 1. Backend — service de génération de miniatures

- [x] 1.1 Créer `backend/services/thumb_service.py` avec la fonction `generate_thumbnails(session_id: str) -> list[str]` qui déchiffre le PDF en mémoire, génère les PNG via `pdf2image.convert_from_bytes()` au `THUMB_DPI` configuré, et écrit les fichiers dans `{TEMP_DIR}/{session_id}/thumbs/page_{n}.png`
- [x] 1.2 Implémenter la logique de cache dans `generate_thumbnails` : vérifier si `thumbs/` existe et contient déjà les fichiers avant de (re)générer
- [x] 1.3 Importer `THUMB_DPI` et `TEMP_DIR` depuis `config.py` (aucune valeur hardcodée)

## 2. Backend — route /thumbs

- [x] 2.1 Créer `backend/routes/thumbs.py` avec `GET /thumbs/{session_id}` qui appelle `generate_thumbnails()` et retourne `{ "urls": ["/thumbs/{session_id}/1", …] }` avec statut 200, ou 404 si la session est inconnue
- [x] 2.2 Ajouter `GET /thumbs/{session_id}/{page}` dans `thumbs.py` qui sert le fichier `page_{page}.png` avec `FileResponse` et `media_type="image/png"`, ou 404 si introuvable
- [x] 2.3 Enregistrer le router `thumbs` dans `backend/main.py` (`app.include_router(thumbs_router)`)

## 3. Frontend — proxy et configuration

- [x] 3.1 Ajouter `'/thumbs': 'http://localhost:8000'` dans le bloc `proxy` de `vite.config.ts`

## 4. Frontend — PageGrid.vue

- [x] 4.1 Ajouter le prop `sessionId: string` à `PageGrid.vue`
- [x] 4.2 Ajouter `thumbUrls: ref<string[]>([])` et un `watch` sur `sessionId` qui appelle `GET /thumbs/{sessionId}` dès que la valeur est non vide
- [x] 4.3 Réinitialiser `thumbUrls` à `[]` quand `sessionId` change (nouveau PDF uploadé)
- [x] 4.4 Passer `:thumb-url="thumbUrls[n - 1]"` à chaque `<PageCard>` dans le template

## 5. Frontend — PageCard.vue

- [x] 5.1 Ajouter le prop optionnel `thumbUrl?: string` à `PageCard.vue` (destructuration réactive Vue 3.5)
- [x] 5.2 Afficher `<img :src="thumbUrl" />` en fond de carte quand `thumbUrl` est défini, avec `object-fit: cover` et taille adaptée à la carte
- [x] 5.3 Conserver le numéro de page en overlay (position absolute, centré en bas) visible dans les deux états (avec ou sans miniature)
- [x] 5.4 Conserver l'état de sélection (bordure bleue, checkmark) indépendamment de la présence de la miniature

## 6. Frontend — App.vue

- [x] 6.1 Passer `:session-id="sessionId"` au composant `<PageGrid>` dans `App.vue`

## 7. Tests

- [x] 7.1 Tester via curl que `GET /thumbs/{session_id}` retourne bien un JSON d'URLs après un upload
- [x] 7.2 Tester via curl que `GET /thumbs/{session_id}/1` retourne un PNG valide
- [x] 7.3 Tester via MCP Puppeteer : uploader un PDF, vérifier que les miniatures s'affichent dans la grille
- [x] 7.4 Tester via MCP Puppeteer : vérifier que la sélection fonctionne avec les miniatures affichées
