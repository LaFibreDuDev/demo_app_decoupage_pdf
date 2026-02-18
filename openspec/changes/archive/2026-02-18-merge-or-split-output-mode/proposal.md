## Why

Actuellement, le découpage génère toujours un seul PDF fusionnant toutes les pages sélectionnées. Certains utilisateurs souhaitent au contraire récupérer chaque page (ou chaque sélection) dans un fichier PDF distinct — cas d'usage courant pour distribuer des pages individuellement ou archiver des sections séparément.

## What Changes

- Ajout d'un sélecteur de mode de sortie dans l'interface : **"Fichier fusionné"** (comportement actuel) ou **"Fichiers séparés"**.
- En mode "Fichiers séparés", le zip retourné contient un PDF par page sélectionnée (nommés individuellement), au lieu d'un PDF unique.
- Le paramètre de mode est transmis au backend via `POST /split` (`output_mode: "merged" | "separate"`).
- Le backend adapte la génération du zip selon le mode choisi.

## Capabilities

### New Capabilities
- `output-mode-selection` : Sélecteur UI permettant à l'utilisateur de choisir le mode de sortie (fusionné ou fichiers séparés) avant de déclencher le téléchargement.

### Modified Capabilities
- `pdf-split` : Le comportement de génération du zip change pour supporter deux modes de sortie ; le contrat de l'endpoint `POST /split` est étendu avec le champ `output_mode`.

## Impact

- **Backend** : `routes/split.py`, `services/pdf_service.py` — logique de génération du zip étendue.
- **Frontend** : `DownloadButton.vue` (ou composant parent) — ajout du sélecteur de mode ; `services/api.ts` — ajout du champ `output_mode` dans la requête.
- **Modèles** : `models.py` — extension du modèle `SplitRequest` avec `output_mode`.
- **Pas de nouvelle dépendance** : pikepdf et zipfile (stdlib) suffisent pour les deux modes.
