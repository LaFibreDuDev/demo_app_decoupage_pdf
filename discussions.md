Sur l’utilisateur

Qui utilisera cette application ? tout le monde
Quelle est la taille typique des fichiers PDF qu’ils veulent découper ? quelques pages (pas d'énormes fichiers)
Vont-ils utiliser l’application sur mobile, desktop, ou les deux ? (les deux, avec une préférence pour le desktop)
Ont-ils besoin d’une interface simple et rapide, ou de fonctionnalités avancées ? une interface simple et rapide, avec des fonctionnalités avancées en option

Sur les fichiers PDF

Quels types de PDF seront traités ? PDF scannés et PDF natifs (mixte de texte et d’images)
Faut-il gérer des PDF protégés par mot de passe ? Non, pas dans la première version
Quelle taille maximale de fichier doit-on accepter ? 10 Mo pour la première version, avec possibilité d’augmenter par la suite
Faut-il préserver la qualité des images dans les PDF découpés ? Oui, la qualité doit être préservée autant que possible

Sur le découpage

L’utilisateur veut-il découper ? par plage de pages (ex : pages 1-3, 5-7) ou par sélection de pages individuelles (ex : pages 1, 3, 5)
Veut-il renommer les fichiers automatiquement après découpage ? Oui, avec un format de nommage clair (ex : originalfilename_page1-3.pdf)
Faut-il permettre de fusionner les pages découpées en un seul fichier PDF ? Non


Sur le téléchargement

Doit-on proposer un téléchargement individuel ou un zip regroupant tous les fichiers ? Un zip regroupant tous les fichiers serait plus pratique pour l’utilisateur
Faut-il envoyer le zip par e-mail ou juste le proposer en téléchargement direct ? Proposer un téléchargement direct serait plus rapide et plus simple pour l’utilisateur
Veut-on une expiration automatique des fichiers pour des raisons de stockage et sécurité ? Oui, les fichiers devraient être supprimés automatiquement après 24 heures pour éviter l’encombrement du serveur et garantir la confidentialité des données.

Sur la sécurité et la confidentialité

Les fichiers PDF contiennent-ils des informations sensibles ? Oui, il est possible que les fichiers contiennent des informations sensibles, il est donc crucial de garantir la confidentialité et la sécurité des données.
Faut-il garantir que les fichiers ne sont pas stockés sur le serveur après téléchargement ? Oui, les fichiers devraient être supprimés immédiatement après le téléchargement pour garantir la confidentialité et la sécurité des données.
Faut-il chiffrer les fichiers temporairement sur le serveur ? Oui, les fichiers devraient être chiffrés temporairement sur le serveur pour garantir la sécurité des données pendant le traitement.

Sur l’UX/UI

L’interface doit-elle être drag & drop pour l’upload ? Oui, une interface drag & drop serait plus intuitive et rapide pour les utilisateurs.
Veut-on un aperçu des pages avant découpage ? Oui, un aperçu des pages serait très utile pour que les utilisateurs puissent sélectionner les pages à découper avec précision.
Faut-il permettre à l’utilisateur de sélectionner rapidement plusieurs pages ? Oui, il serait utile de permettre à l’utilisateur de sélectionner rapidement plusieurs pages, par exemple en utilisant des cases à cocher ou une sélection par glisser-déposer dans l’aperçu des pages.

Ajoute ces informations dans mon @CLAUDE.md ne retouche pas à l'existant 
dans le fichier.

Aperçu de l'objectif du projet

Aperçu de l'architecture globale

Style visuel :
- Interface claire et minimaliste
- Pas de mode sombre pour le MVP

Contraintes et Politiques :
- NE JAMAIS exposer les clés API au client 

Dépendances :
- Préférer les composants existants plutôt que d'ajouter de nouvelles 
bibliothèques UI

À la fin de chaque développement qui implique l'interface graphique :
- Tester avec le MCP Puppeteer, l'interface doit être responsive, fonctionnel et répondre au besoin développé

Documentation :
- Ajoute une section documentation avec les liens vers @PRD.md & @ARCHITECTURE.md 

Context7 :
Utilise toujours context7 lorsque j'ai besoin de génération de code, d'étapes de configuration ou d'installation, ou de documentation de bibliothèque/API. Cela signifie que tu dois automatiquement utiliser les outils MCP Context7 pour résoudre l'identifiant de bibliothèque et obtenir la documentation de bibliothèque sans que j'aie à le demander explicitement.

Note : Toutes les spécifications doivent être rédigées en français, y compris les specs OpenSpec (sections Purpose et Scenarios). Seuls les titres de Requirements doivent rester en anglais avec les mots-clés SHALL/MUST pour la validation OpenSpec.