## Context

L'interface actuelle utilise un layout linéaire vertical centré dans `App.vue`, avec les composants `UploadZone`, `PageGrid` et `DownloadButton` empilés. Il n'y a pas de header, pas de sidebar, pas de dark mode, et les icônes sont des SVGs inline.

La maquette de référence (`docs/design/code.html`, `docs/design/screen.png`) définit un layout entièrement différent : header sticky + sidebar gauche + zone principale avec grille de pages.

Le projet utilise Vue 3 + Vite + TypeScript + Tailwind CSS v3. Aucun store global (Pinia) n'est en place — l'état est géré via props/emit dans `App.vue`.

## Goals / Non-Goals

**Goals:**
- Implémenter le layout sidebar + zone principale tel que défini dans la maquette
- Ajouter le dark mode via Tailwind `darkMode: 'class'`
- Intégrer Material Symbols Outlined (Google Fonts CDN) en remplacement des SVGs inline
- Refactoriser les composants existants pour s'adapter au nouveau layout sans changer la logique métier
- Ajouter les nouveaux composants : `AppHeader`, `AppSidebar`, `PageToolbar`, `UploadToast`
- Ajouter sélection rapide (paires/impaires/réinitialiser) et contrôles de zoom

**Non-Goals:**
- Ne pas changer la logique backend (aucun endpoint modifié)
- Ne pas introduire de store global (Pinia) — l'état reste géré en local dans `App.vue`
- Ne pas implémenter d'animation complexe ou de transition entre états

## Decisions

### D1 — Restructuration de App.vue comme orchestrateur

`App.vue` reste le composant racine qui possède tout l'état applicatif (`sessionId`, `pageCount`, `originalFilename`, `selectedPages`, `outputMode`, `zoomLevel`, `darkMode`, `showToast`). Les nouveaux composants reçoivent des props et émettent des événements.

**Raison :** évite d'introduire Pinia pour un périmètre MVP. La hiérarchie reste simple et lisible.

### D2 — Architecture des nouveaux composants

Nouveaux composants à créer :
- `AppHeader.vue` : header sticky (logo, toggle dark mode, bouton Aide)
- `AppSidebar.vue` : sidebar avec Configuration, Sélection rapide, Sécurité, stats + bouton Télécharger
- `PageToolbar.vue` : barre au-dessus de la grille (nom du fichier, badge pages, contrôles zoom)
- `UploadToast.vue` : toast fixe en bas de page

Composants existants refactorisés :
- `PageGrid.vue` : suppression de son propre header (titre + "Tout sélectionner") — ces contrôles migrent dans `AppSidebar`. Expose `selectEven()`, `selectOdd()`, `clearSelection()`, `selectAll()`.
- `PageCard.vue` : refonte visuelle (border-4, ring, grayscale sur non-sélectionné, badge numéro, label "Inclus")
- `DownloadButton.vue` : logique de téléchargement extraite dans un composable ou conservée directement dans `AppSidebar.vue` (props `sessionId`, `selectedPages`, `outputMode`)
- `UploadZone.vue` : conservé, intégré dans l'état initial de la zone principale (avant upload)

### D3 — Dark mode via Tailwind `darkMode: 'class'`

La classe `dark` est ajoutée/retirée sur `document.documentElement` au clic du bouton dans `AppHeader`. L'état est persisté dans `localStorage` et restauré au chargement via un script inline dans `index.html` (avant le rendu Vue) pour éviter le flash.

**Alternative écartée :** `darkMode: 'media'` — ne permet pas de toggle utilisateur.

### D4 — Icônes via Material Symbols Outlined

Remplacement des SVGs inline par `<span class="material-symbols-outlined">icon_name</span>`. Le lien Google Fonts est ajouté dans `index.html` :

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet"/>
```

**Raison :** cohérence avec la maquette de référence, zéro dépendance npm supplémentaire.

### D5 — Police Inter via Google Fonts

Ajout dans `index.html`, configuration dans `tailwind.config.js` :
```js
fontFamily: { display: ['Inter', 'sans-serif'] }
```
Appliqué via `font-display` sur le `<body>`.

### D6 — Zoom de la grille de pages

Le zoom est implémenté comme un nombre de colonnes variable dans la grille CSS, contrôlé par un `ref<number> zoomLevel` (valeurs : 1 à 5, défaut : 3). Les contrôles +/- dans `PageToolbar` incrémentent/décrément ce niveau. L'affichage en pourcentage est calculé : `[60%, 70%, 80%, 90%, 100%]`.

**Alternative écartée :** transform CSS `scale()` — complique le scroll et la mise en page.

### D7 — Toast de notification upload

`UploadToast` est un composant avec `v-if="showToast"` et position `fixed bottom-8`. Il reçoit `filename` et `fileSize` en props et émet `@close`. Dans `App.vue`, `showToast` est passé à `true` après un upload réussi, avec auto-fermeture après 5 secondes via `setTimeout`.

### D8 — Extension de la configuration Tailwind

`tailwind.config.js` est mis à jour :
```js
darkMode: 'class',
theme: {
  extend: {
    colors: { primary: '#2563eb', 'background-light': '#f8fafc', 'background-dark': '#0f172a' },
    fontFamily: { display: ['Inter', 'sans-serif'] },
    borderRadius: { DEFAULT: '0.75rem' },
  }
}
```

## Risks / Trade-offs

- **Flash of unstyled dark mode** → Mitigé par le script de restauration du thème dans `index.html` avant le mount Vue.
- **Dépendance Google Fonts (CDN externe)** → En environnement sans internet, les polices et icônes ne chargent pas. Acceptable pour le MVP ; une migration vers des assets locaux peut être faite ultérieurement.
- **UploadZone dans la grille** → Dans la maquette, une carte "Ajouter PDF" en fin de grille permet d'uploader un second PDF. Pour le MVP, cette carte est présente visuellement mais ne déclenche pas de logique supplémentaire (un seul PDF à la fois supporté par le backend).
- **Refactorisation de DownloadButton** → La logique de téléchargement (fetch `/split`) est actuellement dans `DownloadButton.vue`. Elle sera copiée dans `AppSidebar.vue` pour simplifier l'intégration, et `DownloadButton.vue` peut être supprimé ou conservé vide.
