dictStats={1:[],2:["jour","mois","annee","global","count","perso","random","hideme","blindme"],3:["messages","messperiods","messevol","messjours","messroles"],4:["voice","voicperiods","voicevol","voicjours","voicroles"],5:["salons","saloserv","saloperiods","saloevol","saloperso","saloroles"],6:["freq","freqserv","freqperiods","freqevol","freqperso","freqroles"],7:["voicechans","vchaserv","vchaperiods","vchaevol","vchaperso","vcharoles"],8:["emotes","emotserv","emotperiods","emotevol","emotperso","emotroles"],9:["reactions","reacserv","reacperiods","reacevol","reacperso","reacroles"],10:["mots","motsperiods","motsevol","motsroles"],11:["divers","diveserv","diveperiods","diveperso","diveroles"],12:["mentions","mentperiods","mentperso","moyheure","moyjour","moymois","moyannee"]}

dictPoll={1:[],2:["poll","polltime"],3:["giveaway","gareroll"],4:["reminder"]}

dictOutils={1:[],2:["tableau","tableau add","tableau del","tableau nb","tableau chan"],3:["twitch","twitch add","twitch del","twitch chan","twitch edit"],4:["customcmd","customcmd add","customcmd del","customcmd embed","customcmd edit","customcmd auteur","customcmd titre","customcmd bas","customcmd image","customcmd miniature","customcmd couleur","customcmd len","customcmd patron"],5:["auto","auto add","auto del","auto edit"]}

dictJeux={1:[],2:["trivial","trivialversus","trivialbr","trivialparty","trivialstreak"],3:["tortues","tortuesduo"],4:["p4","bataillenavale"],5:["jeuxrank","jeuxmondial","trivialrank","trivialperso"]}

dictSV={1:[],2:["savezvous","savezvous add","savezvous del","savezvous edit"],3:["savezvous list","savezvous modo"]}

dictUtile={1:["help","about","invite","support","test","feedback","perms","servcount","credits","reseaux"]}

dictMAL={1:[],2:["maluser","mallist","malcompare","malsearch"]}

dictWiki={1:[],2:["wikipedia","events","wikinsfw"],3:["wikiquote","wikiqotd"]}

dictSpotify={1:[],2:["spoartiste","spoalbum","spoplaylist","spopodcast","spotitre"]}

dictGeo={1:[],2:["iss","nasaphoto"]}

dictAdmin={1:[],2:["hide","blind","mute"],3:["modulestat","modulecmd"],4:["delstats","statson","statsoff"],5:["zip","wikinsfw"]}

dictAutre={1:["roulette","dice","snipe","avatar","say","zeynah"]}

dictPStats={1:"Olbor Track est capable de capter différentes statistiques comme les messages envoyés par chaque membre du serveur, le temps passé en vocal, les emotes utilisées par exemple.\nCes statistiques sont stockées sous plusieurs formes, et consultables avec ces commandes.\nLes administrateurs peuvent les configurer (voir OT!help admin).\n\n**Sous les commandes apparaitront des réactions :**\n <:otGAUCHE:772766034335236127> / <:otDROITE:772766034376523776> : changer de page\n<:otGRAPH:772766034558058506> : afficher les graphiques\n<:otTRI:833666016491864114> : changer le tri\n<:otMOBILE:833736320919797780> : changer l'affichage : classique ou mobile"}
dictPPoll={1:"Olbor Track dispose de plusieurs commandes pour faire des sondages et giveaway.\nPour pouvoir les lancer, il faut avoir la permission 'gestion des messages' sur le serveur.\nLa commande OT!reminder ne nécessite aucune permission spéciale."}
dictPJeux={1:"Olbor Track possède plusieurs jeux qui se jouent à plusieurs, de 2 à 15 joueurs !\nEssayez des jeux Trivial, la Course des Tortues, le Puissance 4 ou la Bataille Navale !\nTous les jeux possèdent des classements par serveurs et mondial !"}
dictPOutils={1:"Olbor Track peut améliorer votre serveur avec des outils pratiques !\nEssayez les tableaux d'emotes, les commandes personnalisées, les alertes Twitch et les commandes automatiques !\nIl faut avoir la permission 'gestion des messages' sur le serveur pour pouvoir les configurer."}
dictPSV={1:"Olbor Track vous permet d'avoir une boîte de connaissance commune à votre serveur !\nN'importe qui peut y ajouter des phrases et/ou des images, qui sortent ensuite aléatoirement avec la commande OT!savezvous.\nLes modérateurs peuvent supprimer des phrases de la boîte."}
dictPUtile={}
dictPMAL={1:"Olbor Track possède des intéractions avec MyAnimeList, pour faire des recherches sur des mangas ou animes et sur des utilisateurs du site !"}
dictPWiki={1:"Olbor Track possède des intéractions avec Wikipedia, pour faire des recherches sur un article, ou alors regarder les événements qui se sont passés aujourd'hui à cette date !"}
dictPSpotify={1:"Olbor Track possède des intéractions avec Wikipedia, pour faire des recherches sur des artistes/albums/titres et + !"}
dictPGeo={1:"Olbor Track possède quelques commandes liées à l'espace : une qui vous donne la photo astronomique du jour, et une autre qui vous montre où se trouve l'ISS en orbite actuellement !"}
dictPAdmin={1:"Les administrateurs du serveur peuvent configurer Olbor Track afin d'avoir une utilisation personnalisée du bot.\nIls peuvent moduler les statistiques traquées, les commandes activées, le statut des salons, et +..."}
dictPAutre={}

dictFStats={1:[],2:["periodes"],3:["periodes","roles"],4:["periodes","roles"],5:["periodes","salons","roles"],6:["periodes","heure","roles"],7:["periodes","voice","roles"],8:["periodes","emote","roles"],9:["periodes","emote","roles"],10:["periodes","roles"],11:["periodes","divers","roles"],12:["periodes"]}

dictFPoll={1:[],2:["temps","texte"],3:["temps","gagnants"],4:["temps"]}

dictFOutils={1:[],2:["salon"],3:["salon"],4:[],5:["salon"]}

dictFJeux={1:[],2:[],3:[],4:[],5:["periodes","jeux"]}

dictFSV={1:[],2:[],3:[]}

dictFUtile={1:[]}

dictFMAL={1:[],2:[]}

dictFWiki={1:[],2:[],3:[]}

dictFSpotify={1:[],2:[]}

dictFGeo={1:[],2:[]}

dictFAdmin={1:[],2:["salon"],3:[],4:[],5:[]}

dictFAutre={1:[]}

dictFields={
    "periodes":{"name":"Gestion des périodes","value":"'mois' : donne le mois actuel\n'annee' : donne l'année actuelle\n[mois] [année] : donne le mois que l'on veut *(ex : février 2020)*\n[année] : donne l'année que l'on veut *(ex : 2021)*"},
    "roles":{"name":"Pour chercher un rôle","value":"- Le mentionner\n- Donner son nom, le bot cherchera le rôle qui correspond."},
    "voice":{"name":"Pour chercher un salon vocal","value":"Donner le nom du salon vocal, le bot cherchera celui qui correspond."},
    "salons":{"name":"Pour chercher un salon textuel","value":"Mentionner le salon."},
    "heure":{"name":"Pour chercher une heure","value":"Donner une heure sous la forme [heure]h.\nExemples : 21h, 1h, 13h, ..."},
    "emote":{"name":"Pour chercher une emote","value":"Ecrire l'emote que l'on veut."},
    "divers":{"name":"Pour chercher une stat diverse","value":"Regarder dans avec la commande OT!divers quelles stats existent, puis donner le nom de celle que l'on veut."},
    "temps":{"name":"Instructions pour le temps","value":"Indiquer un nombre suivi de s (pour secondes) ou m (pour minutes) ou h (pour heures) ou j (pour jours). Si vous voulez mettre des nombres à virgule, utilisez un point (.).\nExemples : 20m (20 minutes), 1.5j (1 jour et 12 heures), 10h (10 heures)"},
    "texte":{"name":"Instructions pour le texte","value":"Pour le bot, chaque mot correspond à une proposition. Si vous voulez poser une question et/ou avoir des propositions plus longues que un seul mot, ajoutez des guillemets (\" \") aux deux extrèmités de chaque proposition."},
    "gagnants":"Comment avoir plusieurs gagnants ?","value":"A la fin de la commande, donnez le nombre de gagnants que vous souhaitez suivi de 'g'.\nExemples : 2g (2 gagnants), 10g (10 gagnants).",
    "jeux":{"name":"Liste des jeux","value":"trivialversus, trivialparty, trivialbr, tortues, tortuesduo, p4, bataillenavale"}}