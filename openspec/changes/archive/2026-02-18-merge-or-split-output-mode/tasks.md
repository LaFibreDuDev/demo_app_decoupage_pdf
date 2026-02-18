## 1. Backend — Modèle et contrat API

- [x] 1.1 Ajouter le champ `output_mode: Literal["merged", "separate"] = "merged"` dans `SplitRequest` (models.py)

## 2. Backend — Service PDF

- [x] 2.1 Ajouter la fonction `split_pdf_separate(session_id, original_filename, pages) -> list[tuple[bytes, str]]` dans `pdf_service.py` : pour chaque page, créer un PDF à une page et retourner la liste `(pdf_bytes, filename)` avec le pattern `{basename}_page{N}.pdf`

## 3. Backend — Route /split

- [x] 3.1 Adapter `routes/split.py` : si `output_mode == "separate"`, appeler `split_pdf_separate()` et itérer sur la liste pour remplir le zip ; si `merged`, conserver le comportement actuel via `split_pdf()`

## 4. Frontend — Sélecteur de mode

- [x] 4.1 Ajouter un `ref<'merged' | 'separate'>` initialisé à `'merged'` dans `DownloadButton.vue`
- [x] 4.2 Ajouter le sélecteur de mode dans le template (deux options radio ou toggle) : "Fichier fusionné" / "Un fichier par page", au-dessus du bouton de téléchargement
- [x] 4.3 Inclure `output_mode` dans le body JSON de la requête `POST /split`
- [x] 4.4 Réinitialiser `output_mode` à `'merged'` après un téléchargement réussi (dans l'émission de `download-success`)

## 5. Tests interface

- [x] 5.1 Vérifier avec Puppeteer : le sélecteur est visible après chargement d'un PDF
- [x] 5.2 Vérifier avec Puppeteer : le téléchargement en mode "fusionné" fonctionne (comportement actuel conservé)
- [x] 5.3 Vérifier avec Puppeteer : le téléchargement en mode "fichiers séparés" déclenche bien une requête avec `output_mode: "separate"`
