![OT](https://cdn.discordapp.com/attachments/726034739550486618/886654310199464036/blue.png)
# Olbor Track 3.2 | Mise à jour "Sobre"
## Introduction
Bonjour cher lecteur. Cela fait plus de 5 mois depuis la dernière grande mise à jour de Olbor Track, la 3.1. Entre temps il s'est passé beaucoup de choses.

Tout d'abord, le bot est vérifié depuis le 7 décembre ! Je suis très fier de cela, ça faisait énormement de temps que je courais après sans succès.

Ensuite, discord.py a annoncé son retour avec une prise en charge des commandes slash et de toutes les nouveautées de l'API Discord. Cela va permettre au bot d'évoluer encore plus. Mais j'y reviendrai dans la conclusion.

Cette mise à jour apporte des nouveautées, bien sûr, mais surtout des suppressions. Le bot était extrêmement chargé en modules et commandes, dont une grande partie ne servait à rien, à part me permettre de toucher à certaines API quand j'ai commencé le projet. Il y a aussi une grande rénovation du code, notamment autour des jeux. Parmis les ajouts majeurs, le module de sondages se retrouve très renforcé, avec de nouvelles possibilités et un tout nouvel outil.

Découvrons tout ça !

## Résumé du patch note
***Suppressions :***
- Module Geo
- Module MyAnimeList
- Module Spotify
- Module Wikipedia
- Bataille Navale
- Code Names
- Stats de mentions
- Commandes de comparaison
- Commandes de stats de rôles

***Sondages :***
- Nouveaux affichages
- Supporte les images dans l'invocation de la commande, pour illustrer les sondages et giveaways
- Nouvelles commandes : `OT!vote` / `OT!election`
- Assistant pour créer les sondages : `OT!pollassistant`
- Nouvelle fonctionnalité, pétition : `OT!petition`
- Le temps max d'un sondage passe de 30 jours à 90 jours
- Les membres non modérateurs peuvent désormais déclencher la commande `OT!poll`

***Jeux / Titres :***
- Nouveau jeu : OT!morpion
- Nouveaux jeux cross-serveur : `OT!morpioncross`, `OT!matricecross`
- Cartes de victoire améliorées
- Prix des outils de personnalisation ajustés
- Fonctionnement des jeux harmonisé

***Outils :***
- Nouvel outil : Icones Dynamiques
- Salons vocaux éphémères v2
- Affichage des tableaux modifié
- [ADMIN] Salons tableaux-masqués

***Stats :***
- Nouvelle commande : `OT!recap`
- Nouvelles commandes : `OT!messfirst` / `OT!emotfirst` / ...
- Affichage des badges VIP et Testeur dans les classements
- Retrait de la possibilité de faire `OT!messages aout` ou n'importe quel autre mois

***Savez-vous :***
- Affichage modifié
- Possibilité de sourcer ses phrases : `OT!savezvous source`
- Possibilité de commenter ou mettre à jour des phrases : `OT!savezvous comment`

***Autre :***
- Commande `OT!nasaphoto` conservée
- Commande `OT!events` conservée
- Nouvelles commandes `OT!births` et `OT!deaths`, dérivées de `OT!events`
- Nouvelle gestion des erreurs

## Détails
### Suppressions
Les modules Geo, MyAnimeList, Wiki et Spotify ont été supprimés car dépassés en terme de code, mais surtout pas assez utilisés et outils pour qu'ils restent pertinents dans le bot. Avoir un trop plein de commandes ne fait qu'accentuer de la confusion, déjà présente à mon gout. L'ergonomie de bot est une priorité sur laquelle j'essaie de réfléchir activement.

En ce qui concerne la Bataille Navale : le jeu était trop peu adapté à Discord, avec le système en MP qui était infernal à gérer et à utiliser. Elle fera certainement son retour avec les commandes slash. Pour le Code Names, il faut que je le réécrive et l'améliore, donc pour le moment je préfère le laisser de côté.

Pour les commandes de rôles et de comparaisons, c'est une raison tout autre : la création de Olbor Track Companion, le futur site internet du Bot, qui permetta d'avoir une meilleure interface pour afficher toutes les stats. Je préfère alléger les commandes de stats du bot et laisser ces deux fonctionnalités en exclusivité pour le Companion.

### Sondages
Commande de vote `OT!vote` : cette commande permet d'effectuer un sondage chronométré, exactement comme `OT!polltime`, mais en n'autorisant qu'une seule réponse par personne. Le bot stocke la première réponse de chaque membre, et ne comptabilise pas les suivantes

Commande d'élection `OT!election` : cette commande fonctionne comme `OT!vote`, sauf que les choix sont cachés ! Dès qu'un membre fait son choix, sa réaction disparait, et ses réponses ne seront plus comptabilisées.

Assistant sondage `OT!pollassitant` : cette nouvelle commande vous aide à créer des sondages, étape par étape : question, puis détermination des propositions, image d'illustration, temps, si c'est un vote, une élection, puis enfin le salon de destination du sondage. C'est pour toutes les personnes qui n'ont pas l'experience d'en faire et qui souhaitent être guidés !

Nouvelle fonction pétition `OT!petition` : cette fonctionnalité vous permet de lancer des pétitions sur votre serveur, qui doivent recevoir le nombre de signatures que vous souhaitez en un temps voulu, et affiche les résultats.

![sondages](https://cdn.discordapp.com/attachments/702208752035692654/946473756619059220/Polls.png)

### Jeux
Les jeux ont été harmonisés dans leur fonctionnement, avec quelques changements en terme d'affichage : 
- votre avatar n'est plus affiché sous forme d'emoji à côté de votre nom, mais à la place l'emoji de votre choix
- la couleur sur le côté de l'Embed est par défaut celle de votre choix, sinon celle sur le serveur
- les surnoms du serveur sont affichés au lieu du nom normal
- et d'autres choses minimes...

Nouveau jeu : jouez avec vos amis au `OT!morpion` ! Les règles sont simples : alignez 3 jetons de votre couleur dans un tableau de dimension 3x3 ! Vous pouvez aussi y jouer en cross-serveur avec `OT!morpioncross` !

![morpion](https://cdn.discordapp.com/attachments/752150155276451993/959095670491467807/unknown.png)

Les cartes de victoires ont été améliorées pour ne plus afficher les badges vides que vous n'avez pas, et un changement de disposition des badges en fonction de ceux que vous possédez.

![carte](https://media.discordapp.net/attachments/661948174339932203/954293143048683520/309032693499297802.png?width=1214&height=683)

Les prix des personnalisations ont changé :
- Emote : 50 OT Coins
- Couleur : 50 OT Coins
- Texte carte : 50 OT Coins
- Fond carte : 250 OT Coins
- Surnom personnalisé : 1500 OT Coins

### Outils
Icones dynamiques : pourquoi avoir une icone de serveur statique, banale, dont on ne fait plus attention ? Avec ce nouvel outil, vous pouvez ajouter des images dans le bot, et votre icone sera changée tous les jours, à minuit, avec une rotation parmi les images proposées ! De plus, n'importe quel membre peut en proposer, en attente d'approbation par un modérateur. Ajoutez un salon d'envoi, des descriptions sur les images et possiblement les membres présents, et profitez chaque jour d'une nouvelle icone. Commencez avec `OT!dynicon`

Salons éphémères v2 : séparation en deux commandes de l'outil : `OT!voicehubs` pour paramétrer les hubs, et `OT!voiceephem` pour paramétrer individuellement le salon éphémère dans lequel vous êtes connecté. Vous pouvez désormais pour les hubs définir un pattern de noms qui sera suivi et une limite de membres par défaut. Pour chaque salon créé individuellement, un leader un défini et peut modifier son salon et le vérouiller.

Tableaux : affichage légérement modifié

Autres : quelques ajustements minimes

### Stats
La commande `OT!recap` était déjà publiée depuis fin décembre, dans le cadre de la nouvelle année, mais je l'officialise dans cette mise à jour 3.2 ! Celle ci permet de consulter un résumé court et total de ses stats, à travers tous les serveurs en commun avec le bot.

Nouvel ensemble de commandes : first. Ces commandes permettent de voir l'historique des premiers dans le classement sur chaque mois pour une stat voulue.

![first](https://cdn.discordapp.com/attachments/752150155276451993/959105013362331738/first.png)

### Savez-vous
Le module Savez-Vous prend de l'ampleur ! Il bénéficie maintenant de deux commandes supplémentaires pour améliorer l'expérience du module !
- Sources : possibilité de laisser une source dans les phrases que vous avez ajouté, avec la commande `OT!savezvous source`
- Mise à jour : possibilité de mettre à jour une phrase que vous avez proposé, sans avoir à la modifier : `OT!savezvous comment`
- Commentaire : possibilité pour les autres membres d'ajouter des commentaires sous les phrases, avec l'approbation de l'auteur de chaque phrase. Si plusieurs personnes laissent des commentaires, un seul parmi tous sera affiché au hasard. `OT!savezvous comment`
- Modification de l'affichage par conséquent
- 
![sv](https://cdn.discordapp.com/attachments/726034739550486618/959106760340291614/unknown.png)

## Conclusion et suite
Voici donc la fin de ce patch note. Cela représente pas mal de travail, dont une grande partie invisible car optimisant juste ce qui existe déjà sans toucher à la partie qui vous concerne, en tant qu'utilisateur.

Le bot a encore beaucoup de lacunes, et j'espère pouvoir les corriger dans un futur proche !

Pour le moment je vais me concentrer sur la création du Companion, qui permettra de gérer les outils des serveurs, son profil de jeu, et consulter toutes les stats des serveurs ! Pas de date prévue, mais je donne de temps en temps des aperçus sur le serveur de tests !

La mise à jour 3.3 portera sur les commandes slash et autres outils d'interface mis à disposition par Discord, quand la 2.0 de discord.py sera publiée officiellement ! Et puis quelques autres choses, prévues dans ma tête depuis quelques temps. Mais ce n'est donc pas pour de suite... 

Il est possible que quelques ajouts et corrections de bugs soient fait au bot dans les prochains jours/semaines !

## Merci à vous !
Merci de soutenir Olbor Track ! C'est grace à vous qu'aujourd'hui nous en sommes là, avec une vérification et un bot utilisé de manière quotidienne dans de multiples serveurs !

Prenez soin de vous, et à la prochaine.

OlborEgamorf.
