![OT](https://cdn.discordapp.com/attachments/726034739550486618/886654308735651840/black.png)
# Olbor Track 3.1 - Beta | Mise à jour "Expansion"

## Introduction
Bonjour, je suis OlborEgamorf, le créateur et développeur de Olbor Track. Je vais vous expliquer les fonctionnalités présentes dans cette mise à jour, et vous parler un peu de l'état du bot.

Les derniers jours ont été jonchés de mauvaises nouvelles et déceptions, avec notamment l'annonce de la fermeture de discord.py

Je programme ce bot Discord depuis maintenant presque 1 an et demi, dans mon temps libre et par passion. Le bot a beaucoup évolué depuis ses premiers jours, pour arriver à aujourd'hui, dans sa version 3.1. D'abord simple bot de statistiques très simple, il est désormais en mesure d'envoyer des alertes YT, Twitter et Twitch, de gérer des messages de bienvenue, de faire des graphiques animées et possède des jeux performants avec un éco-système propre et des modes cross-serveur.

Cette mise à jour marque une étape dans son histoire. Jamais il n'a été aussi proche d'être vérifié par Discord, en ayant dépassé 4 fois le seuil nécessaire de 75 serveurs, mais a dû en perdre immédiatement après, car visiblement ça ne suffit pas.

Le but est de se démarquer de la partie statistiques. Elle est très évoluée (peut-être même trop ?), avec énormément de commandes et de graphiques. Donc il était temps de développer le reste du bot, notamment les outils et les jeux. C'est pour cela que j'utilise le terme "Expansion" pour qualifier la mise à jour.

En terme de contenu, cette version apporte beaucoup de nouveautés, et ce sera la dernière comme ça. Je n'ai pas envie de surcharger le bot, et les possibilités laissées par juste les commandes se limitent vite. Il y aura une version 3.2, qui apportera des choses importantes, mais en se concentrant plus sur quelques aspects. Je ne suis pas en mesure de dire s'il y aura une mise à jour 3.3. Il y aura bien sûr toujours des choses à faire, mais beaucoup d'entres elles ne m'intéressent pas, comme faire un module de modération. Vous pourrez en savoir plus à la toute fin du fichier.

Gardez en tête que c'est une bêta, et qu'il reste des bugs et des choses qui seront améliorées.

Ce document pourrait d'ailleurs évoluer au fil des jours.

Voici maintenant une sorte de "patch note" !

## Contenu global

Outils :
- Messages/images de bienvenue et d'adieu
- Alertes YouTube
- Alertes Twitter
- Anniversaires
- Salons vocaux éphémères
- Alertes venant des salons du serveur de test github, avancement et parties-cross-serveur 

Jeux :
- Système de titres et de personnalisation
- Badges et cartes de victoire
- Jeux Cross-Serveurs
- Paris et mises
- Indicatifs de serveurs et proposition de fonds
- Nouveau jeu : Matrice
- Graphiques pour tout les jeux

Autre :
- OT!reminder en version serveur
- Nouveau bouton : choix de page :otCHOIXPAGE: 
- Ajustements et bug fixes

## Développement
## Outils
### Messages/images de bienvenue/d'adieu

C'est pour moi la fonctionnalité majeure de cette mise à jour. L'idée m'est venue en regardant le dashboard de Mee6. Je me suis dit qu'ils avaient tort de faire payer cet outil, alors qu'il apporte une touche de personnalisation spéciale à un serveur. Alors, je l'ai recréé, et même amélioré.

Comme vous pouvez le deviner, les messages de bienvenue se déclenchent quand un nouveau membre arrive sur le serveur, et ceux d'adieux quand un membre le quitte.

Libre à vous d'activer soit les messages de bienvenue, soit d'adieu soit les deux ou encore aucun. Les deux fonctionnent indépendamment, ainsi que les images et phrases que vous ajoutez.

- Avec la commande `OT!bienvenue`, activez les messages de bienvenue
- Avec la commande `OT!bvimage add`, ajoutez des images de bienvenue
- Avec la commande `OT!bvmessage add`, ajoutez des phrases de bienvenue

Sur les images figureront l'avatar de la personne et optionnellement une phrase que vous pouvez configurer. Par la suite, vous pouvez personnaliser la taille et la couleur du texte avec les commandes `edit`.

Vous pouvez ajouter plusieurs phrases et plusieurs images ! Dans ce cas, à chaque fois une image et une phrase seront choisies aléatoirement parmi toutes !

Vous pouvez aussi ajouter seulement des phrases ou seulement des images.

Les phrases aléatoires permettent de créer un système comme Discord le fait, mais en personnalisé pour votre serveur.

Des balises vous permettent de rendre le contenu des phrases dynamique, avec le nom de la personne, du serveur ou encore le nombre de membres sur le serveur.

Pour les messages d'adieu, il faut remplacer `OT!bienvenue` par `OT!adieu` et `OT!bv` par `OT!ad`.

La particularité des messages d'adieu est qu'ils possèdent un filtre noir et blanc par défaut, et une croix sur l'avatar du membre qui a quitté. Le filtre peut être retiré avec la commande `OT!adimage edit`.

Comme pour à peu près tout dans le bot, les modifications se font avec un numéro associé à chaque phrase et image. Il faut fournir le numéro pour pouvoir faire des modifications et des suppressions, qui est trouvable avec `OT!bvimage`, `OT!bvmessage`, `OT!adimage` et `OT!admessage`.

![bienvenue](https://images-ext-2.discordapp.net/external/EDYclVLplmf8iqLKL40x11_EoCX8vszC_EGJowN3Od0/https/pbs.twimg.com/media/E-OqVDKWYAIHwTy.jpg%3Alarge?width=1202&height=676)
![adieu](https://cdn.discordapp.com/attachments/883085160483000321/888866719211348039/AD272054057533833219.png)

### Alertes YouTube, Twitter et OT - `OT!youtube` / `OT!twitter` / `OT!alertesot` 

Avec l'ajout de ces 3 fonctionnalités, j'ai décidé de les séparer des outils, permettant de mieux les distinguer dans la page d'aide, et car ils méritaient une catégorie spéciale. Les alertes Twitch en font aussi partie.

Le fonctionnement est semblable aux alertes Twitch pour les alertes YouTube et Twitter : une commande pour voir les alertes actives, une pour ajouter, une pour supprimer, une pour modifier le salon et une dernière pour modifier la description.

Le système est toujours avec les "numéros" d'alerte.

La différence notable est dans la création d'une alerte. Pour `OT!twitch`, vous devez fournir en même temps le stream, le salon et la description. Pour les nouvelles alertes YT et Twitter, cela se passe par étapes :
- Invocation de la commande avec nom de la chaine/du compte
- Validation que la chaine/compte trouvée est la bonne
- Configuration du salon
- Configuration de la description

Le tout accompagné par des explications sur quoi faire à chaque étape.

Les alertes OT, elles, fonctionnent sur le schéma des commandes automatiques : les 3 types d'alertes sont prédéfinis (github, updates, cross) et on ne peut pas mettre de description personnalisée. La différence majeure avec elles est que OT n'est pas capable de supprimer les webhooks créés depuis la commande. C'est quelque chose d'assez étrange, mais c'est comme ça. Pour modifier ou supprimer une alerte mise en place, l'utilisateur doit lui-même aller dans les paramètres du salon. La démarche est expliquée si vous essayez de le faire. 

![yt](https://cdn.discordapp.com/attachments/726034739550486618/888882927981711381/unknown.png)
![twit](https://cdn.discordapp.com/attachments/726034739550486618/888883104272498749/unknown.png)

### Anniversaires - `OT!anniversaire`

Fonctionnalité toute autre ! Pour faire ce nouveau module, je me suis inspiré de ce que fait notamment Birthday Bot, qui est assez populaire, mais sans copier ni plagier. Cela fonctionne autour de deux choses :
- Un côté modérateur : les modérateurs peuvent décider **d'activer** la fonctionnalité et la paramétrer. `OT!anniversaire active`
- Un côté utilisateur : les utilisateurs peuvent rentrer leur propre date d'anniversaire, la consulter et consulter celle d'autres membres du serveur. `OT!anniversaire set`

Lorsqu'un utilisateur ajoute sa date d'anniversaire, il l'ajoute pour le bot, et fonctionnera pour tous ses serveurs. Le jour venu, un message sera envoyé pour lui fêter, dans les serveurs qu'il a en commun avec le bot, **et qui ont du coup activé la fonctionnalité.**

Je trouve que c'est quelque chose de sympa pour un serveur, et j'espère que ça aura du succès !

![anniv](https://cdn.discordapp.com/attachments/726034739550486618/888883556716261406/anniv.png)

### Salons vocaux éphémères `OT!voiceephem`

Cette nouveauté est assez spéciale ! Je l'ai vue sur quelques serveurs et j'ai essayé de la reproduire. Je dois l'avouer, ça marche plutot bien !

Le principe : avoir un salon "hub", et quand quelqu'un s'y connecte, le bot crée un nouveau salon vocal pour cette personne. Cela permet de gérer des escouades par exemple, sans avoir à créer au préalable des dizaines de salons. Une fois que tout le monde quitte le salon, il se supprime.

Avec Olbor Track, vous pouvez configurer plusieurs hubs, qui donneront naissance à des salons qui ont les mêmes paramètres qu'eux. `OT!voiceephem add` Vous pouvez aussi définir une limite d'utilisateurs pour chaque salon créé par le hub. `OT!voiceephem limit`

Ensuite, vous pouvez modifier le nom des salons qui seront créés ! Par défaut, les noms sont "Salon 1", "Salon 2", ... `OT!voiceephem edit`

Une fois que tout est configuré, admirez la magie !

## Jeux
### Jeux Cross-Serveurs

C'est une révolution. Tout simplement. Les jeux cross-serveurs vous permettent de jouer avec des gens venant d'autres serveurs, depuis n'importe quel serveur. Lancez la commande, et attendez que des personnent rejoignent. Les personnes de votre serveur peuvent aussi la rejoindre !

Avec ça vient un classement des serveurs ! Sur tous les jeux, si vous gagnez vous faites gagner votre serveur ! Le nombre de points est calculé en fonction du nombre de personnes ne venant pas de votre serveur. `OT!jeuxmondial cross`

Les commandes disponibles sont : `OT!tortuescross` `OT!tortuesduocross` `OT!p4cross` `OT!trivialversuscross` `OT!trivialbrcross` `OT!trivialpartycross`

![cross](https://cdn.discordapp.com/attachments/726034739550486618/888883954571149402/unknown.png)

C'est accompagné par un système d'anonymat et de personnalisation :

### Les titres

Vous avez pu déjà les expérimenter si vous avez essayé la première bêta de la 3.1. Les titres sont un moyen d'anonymiser le nom des joueurs dans les classements mondiaux et les parties cross-serveur, tout en leur laissant une certaine liberté.

Certains titres sont déblocables :
- En atteignant des niveaux sur le OT!trivial
- En gagnant des parties de n'importe quel jeu
- En étant premier des classements de n'importe quel jeu
- En étant un donateur du bot

Et les autres sont achetables :
- Boutique qui s'actualise tous les jours : `OT!titre` pour la consulter / `OT!titre achat` pour en acheter
- Vos amis peuvent vous en offrir : `OT!titre gift`
- Vous pouvez vendre vos titres, pour récupérer des OT Coins et placer le titre en boutique : `OT!titre vente`
- Vous pouvez ouvrir des packs de titres, contenant plusieurs titres `OT!titre pack`

Vous pouvez consulter tous vos titres avec `OT!titre perso` et les équiper avec `OT!titre set`. Vous pouvez en équiper qu'un seul à la fois.

Les OT Coins sont une monnaie qui est gagnée en jouant aux jeux du bot !

![titre](https://cdn.discordapp.com/attachments/726034739550486618/888882234780704869/unknown.png)

### Personnalisation

En plus du titre, vous pouvez personnaliser votre couleur, une emote, et un surnom personnalisé !

Si le surnom est payant (4000 OT Coins), la couleur et l'emote sont gratuits !

- `OT!profil custom` : personnalisation du surnom, qui complète le titre
- `OT!profil emote` : personnalisation de l'emote, qui est affiché dans les jeux cross et les graphiques
- `OT!profil couleur` : personnalisation de la couleur, qui est affiché dans les jeux cross et les graphiques

![perso](https://cdn.discordapp.com/attachments/726034739550486618/888884239595089920/unknown.png)

### Cartes de victoire et badges

Autre outil de personnalisation : les cartes de victoire ! Celles ci s'affichent à la fin des parties de jeu et célèbre le vainqueur sous cette forme :
- Avatar du joueur
- Nom du joueur
- Nombre de victoires
- Fond personnalisé `OT!profil fond`
- Badges liés au jeu (voir après)
- Phrase personnalisée `OT!profil texte`

Dans le cas d'un jeu cross-serveur, l'avatar est remplacé par l'emote et le nom par le titre du joueur.

Chaque fond coute 500 OT Coins, avec une boutique associée, qui reste fixe.

![Exemple](https://cdn.discordapp.com/attachments/702208752035692654/886645100443226122/K2tortues.png)

### Badges

Les badges sont une nouvelle manière de récompenser les meilleurs joueurs des différents jeux. Il en existe au total 9 par jeu, plus 2 spéciaux :
- 3 pour le top 3 des classements globaux
- 3 pour le top 3 des classements par années
- 3 pour le top 3 des classements par mois
- Un pour les contributeurs et un autre pour les testeurs

Voici comment fonctionne leur affichage :
- Dans les cartes de victoires : affichage des badges obtenus sur le jeu, avec un espace blanc si le badge n'est pas obtenu
- Dans les classements : affichage du meilleur badge possédé lié au jeu + badges spéciaux

Vous pouvez consulter vos badges avec `OT!profil badges`

Tous les mois, les badges globaux sont redistribués au top 3 !

![badges](https://cdn.discordapp.com/attachments/702208752035692654/886269733077413898/plaque.png)
![classement](https://cdn.discordapp.com/attachments/726034739550486618/888882360077131816/unknown.png)

### Paris et mises

Autre méthode pour gagner des OT Coins : faire des paris et les mises. Les deux se déroulent pendant les jeux mais n'apparaissent pas pour les mêmes personnes.

Les joueurs de la partie en cours peuvent miser des OT Coins, qui seront donnés au vainqueur final.

Les spectateurs, eux, peuvent parier sur le gagnant ! Chaque joueur possède une côte affichée, calculée en fonction de son classement. Passé un certain stade dans le jeu, la côte est masquée et plus personne ne peut parier.

Pour déclencher la procédure, il faut cliquer sur la réaction :otCOINS: pendant une partie !

### Nouveau jeu : `OT!matrice`

Je vous laisse découvrir par vous même, les règles sont affichés quand vous invoquez la commande !

![matrice](https://cdn.discordapp.com/attachments/726034739550486618/888881881322491934/unknown.png)

### Graphiques pour les jeux

Les jeux sont maintenant dotés de graphiques, qui sont calqués sur ceux des stats classiques. Vous donc retrouverez les types de graphiques habituel, en fonction de la période regardée.

Dans les graphiques la couleur, le titre et l'emote configurés de chaque joueur est affiché !

![graphs](https://cdn.discordapp.com/attachments/726034739550486618/888881613998555146/graph.png)

### Indicatifs et propositions de fonds

Il n'y pas que les joueurs qui ont le droit à des options de personnalisation ! Les serveurs disposent aussi de deux commandes, qui peuvent être utilisées par les modérateurs : 

- `OT!indic` : permet de choisir le nom qui sera affiché pour votre serveur dans le classement cross-serveurs ! L'indicatif doit faire 4 caractères maximum, et sera peut-etre utilisé dans le futur pour d'autres choses !
- `OT!fondsubmit` : étant donné que la boutique de fond de base de OT est assez faible, vous pouvez proposer des fonds pour votre serveur ! Faites la commande, puis donnez l'image que vous voulez (de taille 1280x720) pour qu'elle soit proposée ! Si elle est validée, ***uniquement*** les membres de votre serveur pourront l'acheter et le mettre dans leur carte de victoire !

## Autre
### Rappels version serveur

La commande `OT!reminder` a été renommée en `OT!rappelmp` et propose une nouvelle version : `OT!rappel`.

Quand un rappel est demandé avec `OT!rappel`, le message sera envoyé dans le salon où a eu lieu la commande, avec une mention du membre, au lieu d'en message privé ! Le fonctionnement reste le même.

### Nouveau bouton : choix de page

En plus des boutons droite et gauche, vous pouvez désormais choisir directement dans quelle page aller dans les commandes en proposant plusieurs !

![bouton](https://cdn.discordapp.com/attachments/726034739550486618/888879831251578950/unknown.png)

### Amélioration commande d'aide

Nouvelles catégories et sommaire en page 1 des sections spécialisées !

![help](https://cdn.discordapp.com/attachments/726034739550486618/888878614660128818/helpc.png)

## Et après ?

J'ai développé ma vision du futur dans **La Ligne Bleue**
![ligne](https://cdn.discordapp.com/attachments/726034739550486618/888879116475039755/unknown.png)

Je vais suivre ce plan, mais voici ce qui est prévu pour la version 3.2 :
- Nouveau jeu (mystère...)
- Olbor Track Life, le module de bien-être numérique
- Refonte totale des commandes automatiques pour permettre une personnalisation totale

## Merci à vous.

Vraiment, merci. Sans vous rien ne serait possible.

J'espère que cette mise à jour vous plaira !

Prenez soin de vous.

OlborEgamorf
