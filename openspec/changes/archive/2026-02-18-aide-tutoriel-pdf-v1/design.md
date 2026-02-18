## Context

L'application dispose déjà d'un bouton "Aide" dans `AppHeader.vue`, actuellement inerte (pas d'handler). La spec `ui-layout` stipule que ce bouton doit exister dans le header, mais ne définit pas son comportement. Ce changement l'active en ouvrant une modale de tutoriel 3 étapes, implémentée comme un composant Vue autonome sans dépendance externe.

## Goals / Non-Goals

**Goals:**
- Activer le bouton "Aide" pour ouvrir une modale explicative
- Guider l'utilisateur à travers les 3 étapes du flux : charger → sélectionner → télécharger
- Composant autonome, stylé avec Tailwind, cohérent avec l'UI existante (Material Symbols, palette slate/primary)
- Responsive : modale full-screen sur mobile, centrée et dimensionnée sur desktop

**Non-Goals:**
- Aide contextuelle inline ou tooltips sur chaque élément
- Tutoriel interactif pas-à-pas avec progression (prévu V2+)
- Contenu dynamique selon l'état de l'application
- Localisation (FR uniquement en V1)

## Decisions

**Décision 1 : Modale plutôt que page dédiée ou panneau latéral**
Une modale s'intègre sans modifier le layout existant (sidebar + zone principale) et est accessible depuis n'importe quel état de l'application (avant ou après upload). Une page dédiée nécessiterait un routeur (non encore présent).

**Décision 2 : Composant `HelpModal.vue` dédié**
Isoler la modale dans son propre composant évite de surcharger `App.vue` et facilite une évolution vers un contenu plus riche en V2. Le composant reçoit un prop `open` et émet `close`.

**Décision 3 : Flux de communication AppHeader → App → HelpModal**
- `AppHeader` émet `open-help` au clic sur le bouton Aide (déjà en place)
- `App.vue` maintient `helpOpen: ref(false)` et passe la prop à `HelpModal`
- `HelpModal` émet `close` pour fermer (clic sur ×, clic sur backdrop, touche Escape)
Cette chaîne reste cohérente avec le pattern déjà utilisé pour `sidebarOpen` et `showToast`.

**Décision 4 : Contenu statique en 3 étapes numérotées**
Trois étapes suffisent à couvrir le flux complet pour la V1. Les icônes Material Symbols `upload_file`, `touch_app` et `download` illustrent chaque étape de façon intuitive.

## Risks / Trade-offs

- [Risque] La modale bloque l'interaction principale → Mitigation : fermeture par Escape, clic backdrop et bouton ×
- [Trade-off] Contenu statique = pas adaptatif à l'état de l'app → Acceptable en V1, évolution prévue en V2
