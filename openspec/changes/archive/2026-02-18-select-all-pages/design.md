## Context

`PageGrid.vue` affiche déjà un bouton "Tout désélectionner" (visible quand `selectedPages.length > 0`). Le composant expose `clearSelection()` et gère la sélection en interne via `selectedPages` (ref locale). Le changement est entièrement contenu dans ce composant.

## Goals / Non-Goals

**Goals:**
- Ajouter un bouton "Tout sélectionner" visible quand au moins une page n'est pas encore sélectionnée.
- Maintenir la symétrie visuelle et comportementale avec "Tout désélectionner".

**Non-Goals:**
- Exposer `selectAll()` via `defineExpose` (non nécessaire pour ce MVP).
- Modifier le backend ou le contrat API.

## Decisions

### 1. Condition d'affichage du bouton

**Décision** : afficher "Tout sélectionner" quand `selectedPages.length < pageCount` (au moins une page non sélectionnée), y compris quand aucune page n'est sélectionnée.

**Rationale** : l'état "zéro page sélectionnée" est précisément celui où "Tout sélectionner" est le plus utile. La symétrie avec "Tout désélectionner" (masqué quand tout est désélectionné) est cohérente.

**Alternative écartée** : afficher les deux boutons en permanence — crée de la confusion quand les actions n'ont aucun effet (cliquer "Tout sélectionner" quand tout est déjà sélectionné).

### 2. Positionnement

**Décision** : placer "Tout sélectionner" à gauche de "Tout désélectionner", dans le même conteneur flex en haut à droite de la grille.

**Rationale** : regroupe les actions globales au même endroit, lisibilité naturelle gauche→droite (sélectionner avant désélectionner).

### 3. Implémentation

**Décision** : fonction `selectAll()` locale qui assigne `selectedPages.value = Array.from({ length: pageCount }, (_, i) => i + 1)`.

**Rationale** : pattern identique à `clearSelection()`, simple et cohérent.

## Risks / Trade-offs

- Aucun risque significatif. Changement purement additionnel, sans modification de logique existante.
