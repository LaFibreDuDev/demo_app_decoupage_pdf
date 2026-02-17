## Context

Le projet démarre de zéro : le backend FastAPI et le frontend Vue 3 + Vite sont à créer. Cette feature constitue le socle du MVP — sans elle, aucune autre fonctionnalité n'est accessible.

L'architecture est déjà définie dans `ARCHITECTURE.md` : backend Python/FastAPI, frontend Vue 3/Vite/Tailwind, stockage temporaire chiffré AES-256 dans `/tmp/pdf_splitter/`.

## Goals / Non-Goals

**Goals:**
- Créer l'infrastructure backend minimale (FastAPI + routes)
- Implémenter `POST /upload` : réception, validation serveur, stockage chiffré, retour `session_id` + `page_count`
- Créer le composant `UploadZone.vue` avec bouton de sélection et feedback utilisateur
- Validation client : type `application/pdf`, taille ≤ 10 Mo
- Retour visuel : chargement, erreur, succès

**Non-Goals:**
- Drag & drop (V1)
- Miniatures (V1)
- Découpage ou téléchargement (features suivantes)
- Authentification ou gestion de sessions persistantes

## Decisions

**D1 — Chiffrement en upload immédiat**
Le PDF est chiffré dès l'écriture disque (AES-256 via `cryptography`). La clé est stockée en mémoire dans un dictionnaire global keyed par `session_id`. Alternative rejetée : stockage clair (risque sécurité si crash/dump).

**D2 — `python-multipart` pour le form data**
FastAPI exige `python-multipart` pour `UploadFile`. Déjà prévu dans ARCHITECTURE.md.

**D3 — Validation MIME côté serveur**
On vérifie le content-type déclaré ET les magic bytes (en-tête PDF `%PDF-`) avec `pikepdf.open()`. Le client ne peut pas être seul arbitre du type.

**D4 — UUID v4 pour `session_id`**
Identifiant opaque, non devinable, non listable. Stdlib Python, aucune dépendance supplémentaire.

**D5 — Proxy Vite → FastAPI**
En développement, Vite proxy `/api/*` vers `http://localhost:8000` pour éviter les CORS. En prod, Nginx fera le même rôle.

**D6 — Frontend minimal : pas de store Vuex/Pinia**
Pour le MVP, l'état de session (`session_id`, `page_count`) est géré localement dans `App.vue` via `ref`. Pas de state management global nécessaire à ce stade.

## Risks / Trade-offs

- **[Risque] Clé AES en mémoire perdée si redémarrage serveur** → Mitigation : pour le MVP, acceptable ; les sessions sont courtes. En V1, stocker la clé chiffrée dans un fichier séparé ou utiliser un HSM.
- **[Risque] Fichiers `/tmp` non nettoyés si crash** → Mitigation : le service de cleanup sera implémenté en V1 ; pour le MVP, TTL court et suppression manuelle possible.
- **[Trade-off] Validation MIME client redondante** → Améliore UX (feedback immédiat) mais ne remplace pas la validation serveur.
