## 1. Mise à jour UploadResponse — ajout du nom de fichier

- [x] 1.1 Ajouter le champ `original_filename: str` au modèle Pydantic `UploadResponse` dans `backend/models.py`
- [x] 1.2 Mettre à jour `backend/services/pdf_service.py` : la fonction `save_upload` doit sanitiser le nom du fichier (`file.filename`) — caractères alphanumériques, tirets et underscores uniquement — et le retourner en troisième valeur du tuple `(session_id, page_count, original_filename)`
- [x] 1.3 Mettre à jour `backend/routes/upload.py` pour récupérer `original_filename` depuis `save_upload` et l'inclure dans le `UploadResponse` retourné

## 2. Backend — Modèle et service Split

- [x] 2.1 Ajouter le modèle Pydantic `SplitRequest(session_id: str, original_filename: str, pages: list[int])` dans `backend/models.py`
- [x] 2.2 Ajouter la fonction `split_pdf(session_id, original_filename, pages)` dans `backend/services/pdf_service.py` : déchiffrer le PDF de session en mémoire, valider les numéros de pages (1-based, ≤ page_count), extraire les pages avec pikepdf dans un `BytesIO`, construire le nom de fichier (`{basename}_page{X}.pdf` ou `{basename}_page{X}-{Y}-…pdf`), retourner les bytes du PDF extrait et le nom de fichier

## 3. Backend — Route Split

- [x] 3.1 Créer `backend/routes/split.py` : endpoint `POST /split` — valider que la session existe dans `session_keys` (404 sinon), valider que `pages` n'est pas vide (400 sinon), appeler `split_pdf`, construire un zip en mémoire (`zipfile.ZipFile` sur `io.BytesIO`) contenant le PDF extrait
- [x] 3.2 Retourner le zip via `StreamingResponse` (`media_type="application/zip"`, `Content-Disposition: attachment; filename="{basename}_split.zip"`)
- [x] 3.3 Supprimer la session dans un `BackgroundTask` : `shutil.rmtree` sur le répertoire de session et `del session_keys[session_id]`
- [x] 3.4 Enregistrer `split_router` dans `backend/main.py` (`app.include_router(split_router)`)

## 4. Frontend — Composants PageCard et PageGrid

- [x] 4.1 Créer `frontend/src/components/PageCard.vue` : affiche le numéro de page centré, prop `page` (int) et `selected` (bool), émet `toggle` au clic, style visuellement distinct si sélectionné (bordure colorée ou fond)
- [x] 4.2 Créer `frontend/src/components/PageGrid.vue` : prop `pageCount` (int), liste réactive `selectedPages` (tableau d'entiers), affiche une grille de `PageCard`, émet `update:selected-pages` à chaque changement de sélection
- [x] 4.3 Mettre à jour `frontend/src/App.vue` : stocker `originalFilename` reçu de l'upload, afficher `PageGrid` après upload réussi, lier `selectedPages` depuis `PageGrid`

## 5. Frontend — Composant DownloadButton

- [x] 5.1 Créer `frontend/src/components/DownloadButton.vue` : prop `sessionId`, `originalFilename`, `selectedPages`, bouton désactivé si `selectedPages` est vide ou si chargement en cours
- [x] 5.2 Au clic, envoyer `POST /api/split` avec `{ session_id, original_filename, pages }`, afficher un indicateur de chargement et désactiver le bouton pendant la requête
- [x] 5.3 À la réception du zip (réponse blob), créer un `URL.createObjectURL`, déclencher le téléchargement via un lien `<a>` temporaire, puis émettre `download-success` pour que `App.vue` réinitialise la sélection
- [x] 5.4 En cas d'erreur serveur, afficher le message d'erreur et réactiver le bouton
- [x] 5.5 Intégrer `DownloadButton` dans `App.vue` sous la `PageGrid`, lui passer `sessionId`, `originalFilename` et `selectedPages`
