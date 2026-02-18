## 1. Configuration de base

- [x] 1.1 Mettre à jour `frontend/tailwind.config.js` : ajouter `darkMode: 'class'`, couleur `primary` (#2563eb), couleurs `background-light` / `background-dark`, `fontFamily.display` (Inter), `borderRadius.DEFAULT` (0.75rem)
- [x] 1.2 Ajouter dans `frontend/index.html` le lien Google Fonts (Inter + Material Symbols Outlined)
- [x] 1.3 Ajouter dans `frontend/index.html` un script inline anti-FOUC qui lit `localStorage.getItem('theme')` et applique la classe `dark` sur `<html>` avant le mount Vue

## 2. Nouveau composant AppHeader

- [x] 2.1 Créer `frontend/src/components/AppHeader.vue` : header sticky `h-16`, logo (icône `content_cut` + titre "Découpeur PDF"), bouton toggle dark/light mode (icônes `dark_mode` / `light_mode`), bouton "Aide"
- [x] 2.2 Implémenter l'émission de l'événement `@toggle-dark-mode` au clic du bouton

## 3. Nouveau composant PageToolbar

- [x] 3.1 Créer `frontend/src/components/PageToolbar.vue` : reçoit en props `filename`, `pageCount`, `zoomLevel`, `zoomMin`, `zoomMax`
- [x] 3.2 Afficher icône `description` + nom de fichier tronqué + badge "N pages"
- [x] 3.3 Afficher boutons zoom out (`zoom_out`) et zoom in (`zoom_in`) avec le pourcentage courant entre les deux
- [x] 3.4 Désactiver le bouton zoom out si `zoomLevel === zoomMin`, désactiver zoom in si `zoomLevel === zoomMax`
- [x] 3.5 Émettre `@zoom-in` et `@zoom-out` au clic des boutons correspondants

## 4. Nouveau composant UploadToast

- [x] 4.1 Créer `frontend/src/components/UploadToast.vue` : position `fixed bottom-8 left-1/2 -translate-x-1/2`, affiche icône `check_circle` (vert), texte "Document chargé avec succès (X.X Mo)", bouton de fermeture `close`
- [x] 4.2 Recevoir en props `filename` et `fileSizeMo` (nombre)
- [x] 4.3 Émettre `@close` au clic du bouton de fermeture

## 5. Nouveau composant AppSidebar

- [x] 5.1 Créer `frontend/src/components/AppSidebar.vue` avec la structure en sections : Configuration, Sélection, Sécurité & Confidentialité, résumé + bouton download
- [x] 5.2 Section Configuration : deux boutons radio styled ("Fichier fusionné" / "Fichiers individuels"), valeur liée à la prop `outputMode`, émission de `@update:output-mode`
- [x] 5.3 Section Sélection : bouton "Tout sélectionner" + boutons "Pages paires", "Pages impaires", "Réinitialiser" ; émission des événements `@select-all`, `@select-even`, `@select-odd`, `@reset-selection`
- [x] 5.4 Section Sécurité : afficher les deux indicateurs (cadenas + historique) avec icônes Material Symbols
- [x] 5.5 Résumé : afficher "Sélectionné : N pages" lié à la prop `selectedCount`
- [x] 5.6 Bouton Télécharger : affiche "Télécharger (N)", désactivé si `selectedCount === 0`, émet `@download` au clic
- [x] 5.7 Intégrer la logique fetch `/split` dans la sidebar (migré depuis `DownloadButton.vue`) avec gestion du loading et des erreurs

## 6. Refactorisation PageCard

- [x] 6.1 Refondre le template de `PageCard.vue` : border-4 (`border-primary` si sélectionné, `border-transparent` sinon), ring (`ring-4 ring-primary/20`) si sélectionné
- [x] 6.2 Appliquer `grayscale` + `opacity-70` sur l'image et le conteneur si la page n'est pas sélectionnée
- [x] 6.3 Afficher le badge numéro de page (fond bleu + texte blanc si sélectionné, fond gris / bordure si non sélectionné)
- [x] 6.4 Afficher le label "Inclus" en dessous de la card si la page est sélectionnée
- [x] 6.5 Afficher l'overlay "+" au survol d'une page non sélectionnée
- [x] 6.6 Afficher le checkmark en haut à droite si la page est sélectionnée (icône `check` Material Symbols)

## 7. Refactorisation PageGrid

- [x] 7.1 Supprimer le header interne de `PageGrid.vue` (titre + boutons Tout sélectionner / Tout désélectionner)
- [x] 7.2 Ajouter la prop `zoomLevel` (nombre, 1–5) qui contrôle le nombre de colonnes de la grille Tailwind
- [x] 7.3 Ajouter les méthodes exposées `selectEven()` et `selectOdd()` via `defineExpose`
- [x] 7.4 Conserver les méthodes `selectAll()` et `clearSelection()` déjà exposées

## 8. Refactorisation App.vue

- [x] 8.1 Refondre le template d'`App.vue` : `<AppHeader>` + `<main class="flex flex-1 overflow-hidden">` avec `<AppSidebar>` à gauche et zone principale à droite
- [x] 8.2 Ajouter les refs d'état : `darkMode`, `zoomLevel` (défaut : 3), `showToast`, `toastFilename`, `toastFileSizeMo`, `outputMode`
- [x] 8.3 Implémenter `toggleDarkMode()` : bascule la classe `dark` sur `document.documentElement`, persiste dans `localStorage`
- [x] 8.4 Implémenter `onUploadSuccess()` : mettre à jour `sessionId`, `pageCount`, `originalFilename`, déclencher l'affichage du toast avec les infos du fichier
- [x] 8.5 Implémenter la logique de toast : `showToast = true` après upload, `setTimeout` 5s pour `showToast = false`
- [x] 8.6 Connecter les événements de la sidebar (`@select-even`, `@select-odd`, `@reset-selection`, `@select-all`) aux méthodes exposées de `PageGrid` via `pageGridRef`
- [x] 8.7 Connecter `@zoom-in` / `@zoom-out` de `PageToolbar` aux incréments/décréments de `zoomLevel`
- [x] 8.8 Passer `outputMode` en prop à `AppSidebar` et recevoir `@update:output-mode`
- [x] 8.9 Afficher `<UploadToast>` conditionnellement avec `v-if="showToast"` et connecter `@close`
- [x] 8.10 Afficher la zone principale : `<UploadZone>` si pas de session, `<PageToolbar>` + `<PageGrid>` si session active

## 9. Vérification et tests UI

- [x] 9.1 Vérifier le rendu du layout sidebar + zone principale dans le navigateur
- [x] 9.2 Vérifier le toggle dark mode (basculement, persistance au reload, pas de FOUC)
- [x] 9.3 Vérifier les contrôles de zoom (niveaux 1–5, désactivation aux limites, affichage du %)
- [x] 9.4 Vérifier le toast après upload (affichage, auto-fermeture, bouton close)
- [x] 9.5 Vérifier la sélection rapide paires/impaires/réinitialiser
- [x] 9.6 Vérifier les états des cards (sélectionné vs non-sélectionné : bordure, grayscale, badge, label)
- [x] 9.7 Tester le téléchargement depuis la sidebar (bouton Télécharger, loading, résultat)
