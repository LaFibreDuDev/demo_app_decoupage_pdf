## Context

Le backend possède déjà `THUMB_DPI` dans `config.py` et `pdf2image` / Poppler dans les dépendances système. La route `GET /thumbs/` est mentionnée dans l'architecture mais n'existe pas encore. Le frontend affiche une grille de cases numérotées via `PageGrid.vue` + `PageCard.vue` ; aucune image n'est chargée.

## Goals / Non-Goals

**Goals:**
- Générer les miniatures PNG de toutes les pages d'une session en un seul appel backend.
- Servir chaque miniature via une URL individuelle utilisable directement comme attribut `src`.
- Mettre en cache les fichiers générés dans le répertoire de session (pas de regénération à chaque requête).
- Afficher la miniature dans `PageCard.vue` avec le numéro en overlay.

**Non-Goals:**
- Génération progressive (page par page) : toutes les miniatures sont générées en une seule passe.
- Authentification ou signature des URLs de miniatures.
- Support de résolutions multiples ou de redimensionnement dynamique.

## Decisions

### 1. Deux endpoints distincts : liste + image individuelle

**Décision** : `GET /thumbs/{session_id}` retourne un JSON `{ "urls": ["/thumbs/{session_id}/1", …] }`. `GET /thumbs/{session_id}/{page}` retourne le PNG binaire avec `Content-Type: image/png`.

**Pourquoi** : les URLs JSON permettent au frontend de binder chaque URL directement sur `<img src="">`, le navigateur gère lui-même le chargement et le cache HTTP. Alternative rejetée : retourner du base64 dans le JSON — surcharge inutile, pas de cache navigateur.

---

### 2. Génération synchrone à la première requête sur `/thumbs/{session_id}`, mise en cache sur disque

**Décision** : à la réception de `GET /thumbs/{session_id}`, le service vérifie si les fichiers `thumbs/page_{n}.png` existent déjà dans le répertoire de session. S'ils n'existent pas, il déchiffre le PDF en mémoire, génère toutes les pages via `pdf2image.convert_from_bytes()` et écrit les fichiers. Les appels suivants lisent directement depuis le disque.

**Pourquoi** : simple à implémenter, évite la regénération coûteuse. Alternative rejetée : génération à l'upload — allonge inutilement le temps de réponse de `POST /upload`, et les miniatures pourraient ne jamais être demandées.

---

### 3. `PageGrid.vue` appelle `/thumbs/{session_id}` après réception de l'événement `upload-success`

**Décision** : `PageGrid` reçoit `sessionId` en prop (nouveau prop ajouté) et effectue le fetch des URLs dès que `sessionId` est non nul (via `watch`). Les URLs sont stockées dans `thumbUrls: ref<string[]>([])` et transmises à chaque `PageCard` via `:thumb-url="thumbUrls[n-1]"`.

**Pourquoi** : `PageGrid` est déjà responsable de l'affichage des pages — c'est le bon niveau pour posséder les URLs de miniatures. Alternative rejetée : faire le fetch dans `App.vue` et passer les URLs en prop — ajoute une dépendance inutile dans le composant racine.

---

### 4. `PageCard.vue` affiche l'image si disponible, numéro en overlay permanent

**Décision** : `PageCard` reçoit un nouveau prop optionnel `thumbUrl?: string`. Si défini, une balise `<img>` s'affiche en fond de la carte ; le numéro de page reste visible en overlay (position absolute, bas de carte). Si `thumbUrl` est absent ou en chargement, la carte affiche uniquement le numéro (comportement actuel).

**Pourquoi** : dégradation gracieuse — si les miniatures tardent ou échouent, l'UX reste fonctionnelle.

---

### 5. Proxy Vite étendu à `/thumbs`

**Décision** : ajouter `'/thumbs': 'http://localhost:8000'` dans `vite.config.ts`.

**Pourquoi** : cohérent avec `/upload` et `/split` déjà proxifiés.

## Risks / Trade-offs

- **Génération lente pour PDFs volumineux** → `pdf2image` traite toutes les pages en une passe ; acceptable pour le MVP (max 5–10 Mo). Mitigation : le frontend peut afficher un état de chargement pendant le fetch.
- **Espace disque des miniatures** → les fichiers PNG s'accumulent dans `TEMP_DIR` ; le nettoyage automatique existant (TTL 24h) couvre ce risque.
- **Session inconnue ou expirée** → `GET /thumbs/{session_id}` retourne 404 si le répertoire n'existe pas.
