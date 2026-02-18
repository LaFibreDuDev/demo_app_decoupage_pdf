## Context

`PageCard.vue` reçoit une prop optionnelle `thumbUrl`. Lorsque cette prop est absente (miniature pas encore chargée), le composant affiche un fallback basique : fond gris neutre avec le numéro de page centré en gros texte grisé. Ce rendu est pauvre visuellement et ne donne aucune indication de progression.

Le composant `PageGrid.vue` gère le chargement des miniatures via `GET /thumbs/{session_id}` et passe les URLs aux cards une par une à mesure qu'elles arrivent. L'état "loading" est donc naturellement représenté par `thumbUrl === undefined`.

## Goals / Non-Goals

**Goals:**
- Remplacer le fallback texte par un skeleton `animate-pulse` couvrant la zone image de la carte
- Conserver le numéro de page visible en overlay sur le skeleton (cohérence avec l'état chargé)
- Respecter le thème clair/sombre via les classes Tailwind existantes

**Non-Goals:**
- Distinguer "en cours de chargement" d'un "échec de chargement" (V1 : skeleton permanent si erreur)
- Ajouter une prop `isLoading` — la prop existante `thumbUrl` suffit comme indicateur
- Modifier le backend ou PageGrid.vue

## Decisions

### Pas de nouvelle prop — `thumbUrl` comme seul signal
Le skeleton s'affiche quand `thumbUrl` est falsy (undefined ou null). C'est déjà le cas dans le `v-else` existant. Aucun nouveau prop nécessaire.

**Alternatif considéré** : ajouter une prop `isLoading: boolean` distincte pour différencier "chargement" d'une "absence définitive de miniature". Rejeté pour V1 — la complexité n'est pas justifiée, le cas d'erreur permanent est rare et acceptable visuellement.

### `animate-pulse` Tailwind — pas de bibliothèque externe
Tailwind fournit `animate-pulse` nativement. La couleur du bloc skeleton utilise `bg-slate-200 dark:bg-slate-700`, cohérente avec la charte existante.

**Alternatif considéré** : une animation CSS custom (shimmer). Rejeté — `animate-pulse` est suffisant pour V1 et ne nécessite aucun code supplémentaire.

### Numéro de page en overlay sur le skeleton
Le numéro de page (badge en bas à gauche dans le label sous la carte) reste inchangé. À l'intérieur de la zone image, un badge numéro de page en overlay est ajouté sur le skeleton — identique à ce qui sera visible une fois la miniature chargée — pour ancrer visuellement la position de la page.

## Risks / Trade-offs

- **Skeleton permanent en cas d'erreur HTTP** : si `GET /thumbs/{session_id}/{page}` retourne une erreur, `thumbUrl` ne sera jamais défini et le skeleton reste affiché indéfiniment. → Acceptable en V1 ; géré dans une itération future avec un état d'erreur dédié.
- **Transition skeleton → image** : le remplacement `v-if`/`v-else` est abrupt (pas de fondu). → Acceptable en V1 ; une transition CSS `transition-opacity` peut être ajoutée ultérieurement si nécessaire.
