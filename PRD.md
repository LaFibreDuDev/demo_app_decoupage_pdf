# Application de découpage de PDF

## 1. Objectif de l’application
Créer une application permettant à un utilisateur de :  
- Télécharger un PDF de plusieurs pages.  
- Sélectionner des pages individuelles ou des plages de pages.  
- Extraire ces pages dans des fichiers PDF séparés.  
- Télécharger tous les fichiers découpés dans un **zip**.  
- Garantir la sécurité et la confidentialité des fichiers.

---

## 2. Analyse des besoins

### Sur l’utilisateur
- **Qui ?** Tout le monde.  
- **Taille des fichiers PDF ?** Quelques pages (pas d’énormes fichiers).  
- **Plateformes ?** Mobile et desktop, avec préférence pour desktop.  
- **Interface ?** Simple et rapide, avec fonctionnalités avancées optionnelles.

### Sur les fichiers PDF
- **Types de PDF** : scannés et natifs (texte et images).  
- **PDF protégés** : pas dans la première version.  
- **Taille maximale** : 10 Mo pour la première version.  
- **Qualité des images** : à préserver autant que possible.

### Sur le découpage
- **Sélection** : pages individuelles et plages de pages.  
- **Renommage automatique** : oui (`originalfilename_page1-3.pdf`).  
- **Fusion des pages** : non dans la première version.

### Sur le téléchargement
- **Mode** : zip regroupant tous les fichiers.  
- **Téléchargement** : direct depuis le navigateur.  
- **Expiration des fichiers** : suppression automatique côté serveur après 24h.

### Sur la sécurité et la confidentialité
- Les fichiers peuvent contenir des informations sensibles.  
- Les fichiers doivent être supprimés après téléchargement.  
- Les fichiers doivent être chiffrés temporairement sur le serveur.

### UX / UI
- Interface **drag & drop** pour l’upload.  
- **Aperçu des pages** pour sélection précise.  
- Sélection rapide des pages (cases à cocher ou glisser-déposer).

---

## 3. Fonctionnalités par version

### 🟢 MVP (Minimum Viable Product)
- Upload de PDF simple (bouton + validation type/poids).  
- Découpage basique (sélection de pages et extraction).  
- Téléchargement direct des fichiers extraits.

**Pourquoi :** Permettre à l’utilisateur de découper et récupérer un PDF rapidement.

---

### 🟡 V1 (Version fonctionnelle complète)
- Drag & drop pour upload.  
- Aperçu des pages (miniatures).  
- Sélection multi-pages intuitive.  
- Possibilité de choisir entre une fusion des pages sélectionnées ou des fichiers séparés.
- Renommage automatique des fichiers.  
- Téléchargement en zip regroupant tous les fichiers.  
- Sécurité et confidentialité :
  - Fichiers temporaires chiffrés sur serveur.  
  - Suppression automatique après 24h.
- Changement du design en utilisant les fichiers mis à disposition dans le dossier @docs/design.

**Pourquoi :** Expérience complète, pratique et sécurisée pour tous les utilisateurs.

---

### 🔵 V2 (Fonctionnalités avancées / premium)
- Découpage par bookmarks / chapitres.  
- Compression automatique des PDF dans le zip.  
- Support PDF protégés par mot de passe.  
- Fusion des pages sélectionnées en un seul PDF.  
- Notifications ou e-mails pour gros fichiers.

**Pourquoi :** Fonctionnalités avancées pour utilisateurs réguliers ou professionnels.

---

### ⚪ Hors-périmètre
- Édition du contenu PDF (texte, images, annotations).  
- OCR pour rendre éditables les PDF scannés.  
- Gestion multi-utilisateurs ou stockage cloud permanent.  
- Historique des fichiers découpés ou intégration à services externes.

**Pourquoi :** Complexe et non nécessaire pour découpage et téléchargement sécurisé.

---

## 4. Flux utilisateur (conceptuel)
1. L’utilisateur **upload** son PDF via drag & drop ou bouton.  
2. L’utilisateur visualise **l’aperçu des pages**.  
3. L’utilisateur **sélectionne** les pages ou plages de pages à extraire.  
4. L’application **découpe** le PDF et renomme automatiquement les fichiers.  
5. L’utilisateur **télécharge** un zip contenant tous les fichiers.  
6. Les fichiers sont **supprimés** du serveur après téléchargement ou après 24h pour la sécurité.

---

## 5. Points clés pour le développement
- Garder la **simplicité** pour le MVP et la V1.  
- Prioriser **sécurité et confidentialité**.  
- Préparer le code pour **extension future** (V2 et fonctionnalités avancées).  
- UX claire et rapide : drag & drop, aperçu, sélection multiple.
