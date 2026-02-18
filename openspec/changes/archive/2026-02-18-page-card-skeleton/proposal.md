## Why

Lors du chargement des miniatures, chaque carte affiche actuellement uniquement le numéro de page centré sur fond neutre, ce qui offre une expérience visuelle pauvre et donne l'impression que l'interface est figée. Un skeleton animé améliore la perception de performance et signale clairement à l'utilisateur que le contenu est en cours de chargement.

## What Changes

- Le composant `PageCard.vue` remplace l'état intermédiaire "numéro de page centré" par un skeleton animé (animation pulse) couvrant la zone de la miniature.
- Le skeleton respecte les proportions d'une page A4 (ratio portrait) et s'intègre dans le thème clair/sombre existant.
- Le numéro de page reste visible en overlay sur le skeleton, comme il le sera une fois la miniature chargée.
- Aucun changement backend.

## Capabilities

### New Capabilities

_(aucune)_

### Modified Capabilities

- `page-selection` : le requirement "Affichage de la grille de pages après upload" est modifié — l'état intermédiaire pendant le chargement des miniatures passe de "numéro de page centré" à un skeleton animé avec numéro de page en overlay.

## Impact

- `frontend/src/components/PageCard.vue` — ajout de l'état skeleton
- Tailwind CSS : utilisation des classes `animate-pulse` et variantes dark mode existantes
- Aucun impact backend, API, ou autres composants
