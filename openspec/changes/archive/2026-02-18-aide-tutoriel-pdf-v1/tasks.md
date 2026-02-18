## 1. Composant HelpModal.vue

- [x] 1.1 Créer `frontend/src/components/HelpModal.vue` avec prop `open: boolean` et emit `close`
- [x] 1.2 Implémenter le backdrop semi-transparent avec fermeture au clic
- [x] 1.3 Implémenter la fermeture via la touche Escape (listener `keydown` monté/démonté avec `watchEffect`)
- [x] 1.4 Implémenter le bouton de fermeture × en haut à droite du panneau
- [x] 1.5 Intégrer le contenu statique des 3 étapes (icône + numéro + titre + description)
- [x] 1.6 Appliquer le style responsive : pleine largeur sur mobile, centré avec `max-w-lg` sur desktop

## 2. Câblage dans AppHeader.vue

- [x] 2.1 Ajouter l'emit `open-help` dans `defineEmits` de `AppHeader.vue`
- [x] 2.2 Ajouter `@click="$emit('open-help')"` sur le bouton "Aide" existant

## 3. Câblage dans App.vue

- [x] 3.1 Ajouter `helpOpen: ref(false)` dans le script de `App.vue`
- [x] 3.2 Écouter `@open-help="helpOpen = true"` sur `<AppHeader>`
- [x] 3.3 Importer et déclarer `HelpModal` dans `App.vue`
- [x] 3.4 Ajouter `<HelpModal :open="helpOpen" @close="helpOpen = false" />` dans le template

## 4. Vérification

- [x] 4.1 Tester l'ouverture depuis le header en mode desktop (icône + libellé "Aide" visibles)
- [x] 4.2 Tester l'ouverture depuis le header en mode mobile (icône seule)
- [x] 4.3 Vérifier les 3 mécanismes de fermeture : bouton ×, backdrop, touche Escape
- [x] 4.4 Vérifier que la session et la sélection de pages sont préservées après ouverture/fermeture
- [x] 4.5 Tester le responsive de la modale sur mobile (pleine largeur) et desktop (centrée)
