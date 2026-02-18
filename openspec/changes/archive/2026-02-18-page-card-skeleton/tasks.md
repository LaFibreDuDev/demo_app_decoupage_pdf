## 1. Implémentation du skeleton dans PageCard.vue

- [x] 1.1 Remplacer le bloc `v-else` (fallback "numéro centré") par un bloc skeleton `animate-pulse` couvrant la zone image (`aspect-[3/4]`)
- [x] 1.2 Appliquer les couleurs thème : `bg-slate-200 dark:bg-slate-700` sur le bloc skeleton
- [x] 1.3 Ajouter le numéro de page en overlay sur le skeleton (badge positionné en `absolute`, identique à l'overlay sur la miniature)

## 2. Vérification visuelle

- [x] 2.1 Vérifier l'animation pulse en mode clair (fond `bg-slate-200`)
- [x] 2.2 Vérifier l'animation pulse en mode sombre (fond `bg-slate-700`)
- [x] 2.3 Vérifier que le numéro de page est lisible en overlay sur le skeleton
- [x] 2.4 Vérifier que le skeleton respecte le ratio `aspect-[3/4]` de la carte
- [x] 2.5 Vérifier la transition skeleton → miniature lors du chargement réel (uploader un PDF)

## 3. Test Puppeteer

- [x] 3.1 Tester l'affichage du skeleton immédiatement après upload (avant chargement des miniatures)
- [x] 3.2 Vérifier la disparition du skeleton une fois les miniatures chargées
