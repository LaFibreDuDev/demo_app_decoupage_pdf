## Context

Le comportement actuel de `POST /split` produit toujours un zip contenant un unique PDF fusionnant toutes les pages sélectionnées. La logique de découpage est répartie entre `routes/split.py` (construction du zip) et `services/pdf_service.split_pdf()` (extraction pikepdf). Le frontend (`DownloadButton.vue`) envoie `{ session_id, original_filename, pages }` sans notion de mode.

## Goals / Non-Goals

**Goals:**
- Ajouter un champ `output_mode: "merged" | "separate"` au contrat de `POST /split`.
- En mode `separate`, le zip contient un PDF par page sélectionnée.
- En mode `merged`, conserver le comportement actuel (un seul PDF fusionné).
- Exposer un sélecteur de mode dans `DownloadButton.vue` (état local au composant).
- Garder le mode `merged` comme défaut pour ne pas briser l'expérience existante.

**Non-Goals:**
- Grouper des plages (ex. pages 1-3 dans un PDF, pages 5-7 dans un autre) — hors scope V1.
- Persister le choix de mode entre sessions utilisateur.

## Decisions

### 1. Séparation des responsabilités backend

**Décision** : ajouter une fonction `split_pdf_separate()` dans `pdf_service.py`, distincte de `split_pdf()`. La route choisit laquelle appeler selon `output_mode`.

**Rationale** : `split_pdf()` retourne `(bytes, str)` ; le mode séparé retourne `list[tuple[bytes, str]]`. Changer la signature de `split_pdf()` casserait son contrat. Deux fonctions spécialisées sont plus lisibles et testables qu'une fonction avec branchement interne.

**Alternative écartée** : passer `output_mode` à `split_pdf()` et renvoyer une union — plus opaque, plus difficile à typer proprement.

### 2. Construction du zip côté route

**Décision** : la boucle d'ajout des fichiers au zip reste dans `routes/split.py`. En mode `separate`, on itère sur la liste de tuples retournée par `split_pdf_separate()`.

**Rationale** : la route est déjà responsable du zip ; évite de coupler `pdf_service` à `zipfile`.

### 3. Mode de sortie par défaut

**Décision** : `output_mode` est un champ optionnel de `SplitRequest` avec valeur par défaut `"merged"`.

**Rationale** : rétro-compatibilité — les clients qui n'envoient pas ce champ conservent le comportement actuel.

### 4. Sélecteur UI dans DownloadButton.vue

**Décision** : le mode est un `ref` local à `DownloadButton.vue`, exposé via deux boutons radio/toggle au-dessus du bouton de téléchargement. Aucun prop ni emit supplémentaire vers le parent.

**Rationale** : le mode de sortie est une préférence de téléchargement, pas un état partagé de la grille de pages. Le composant est déjà autonome pour la logique de fetch.

### 5. Nommage des fichiers en mode séparé

**Décision** : chaque PDF est nommé `{basename}_page{N}.pdf`, en réutilisant `_sanitize_filename()` existant.

**Rationale** : cohérence avec le pattern de nommage actuel pour une page unique.

## Risks / Trade-offs

- **Taille du zip en mode séparé** : N PDFs déchiffrés en mémoire simultanément. Pour un PDF de 50 pages volumineuses, la RAM consommée peut être significative. → Mitigation : la limite d'upload de 10 Mo sur le PDF source borne la taille totale ; acceptable pour le MVP.
- **UX du sélecteur** : un toggle radio simple peut passer inaperçu. → Mitigation : utiliser un libellé explicite ("Un fichier par page" / "Tout fusionner") avec description courte.
- **Rétro-compatibilité API** : le champ `output_mode` étant optionnel avec défaut, aucun client existant n'est impacté.
