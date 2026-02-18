## ADDED Requirements

### Requirement: Toggle dark/light mode
L'application SHALL proposer un bouton de bascule entre le mode clair et le mode sombre dans le header. Ce bouton MUST afficher une icône de lune (mode sombre) en mode clair, et une icône de soleil (mode clair) en mode sombre. Le toggle MUST s'appliquer instantanément à l'ensemble de l'interface.

#### Scenario: Activation du mode sombre
- **WHEN** l'utilisateur clique sur le bouton de toggle en mode clair
- **THEN** l'interface bascule en mode sombre (arrière-plans sombres, textes clairs)
- **THEN** l'icône du bouton change pour indiquer la possibilité de revenir au mode clair

#### Scenario: Retour au mode clair
- **WHEN** l'utilisateur clique sur le bouton de toggle en mode sombre
- **THEN** l'interface revient en mode clair
- **THEN** l'icône du bouton change pour indiquer la possibilité de passer en mode sombre

### Requirement: Persistance du mode entre sessions
Le mode sélectionné (clair ou sombre) SHALL être persisté dans le `localStorage` du navigateur. Au rechargement de la page, l'application MUST restaurer le dernier mode utilisé sans produire de flash visuel (FOUC).

#### Scenario: Persistance après rechargement
- **WHEN** l'utilisateur a activé le mode sombre et recharge la page
- **THEN** l'interface s'affiche directement en mode sombre sans flash

#### Scenario: Mode clair par défaut
- **WHEN** l'application est chargée pour la première fois (aucune préférence sauvegardée)
- **THEN** l'interface s'affiche en mode clair

### Requirement: Application cohérente du thème sur tous les composants
Tous les composants de l'interface (header, sidebar, grille, cards, boutons, toasts) SHALL répondre aux classes dark mode Tailwind. Aucun composant ne MUST conserver un style fixe indépendant du thème actif.

#### Scenario: Sidebar en mode sombre
- **WHEN** le mode sombre est actif
- **THEN** la sidebar affiche un arrière-plan sombre et des textes clairs

#### Scenario: Cards de pages en mode sombre
- **WHEN** le mode sombre est actif
- **THEN** les cards de la grille affichent un arrière-plan sombre adapté
