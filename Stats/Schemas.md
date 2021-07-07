# Schémas des bases de données SQL pour les stats :

| Type de table  | Schéma |
| ------------- | ------------- |
| evol  | CREATE TABLE evol (Rank INT, ID BIGINT, Jour TEXT, Mois TEXT, Annee TEXT, DateID TEXT, Count INT, Evol INT, PRIMARY KEY(Jour,Mois,Annee)) |
| classement  | CREATE TABLE classement (Rank INT, ID BIGINT PRIMARY KEY, Mois TEXT, Annee TEXT, Count INT, Evol INT)  |
| periods | CREATE TABLE periods (Rank INT, ID BIGINT, Mois TEXT, Annee TEXT, Count INT,PRIMARY KEY(Mois,Annee)) |
| first | CREATE TABLE first (ID BIGINT, Mois TEXT, Annee TEXT, DateID INT, Count INT, PRIMARY KEY(Mois,Annee)) |
| perso | CREATE TABLE perso (Rank INT, ID BIGINT PRIMARY KEY, IDComp BIGINT, Mois TEXT, Annee TEXT, Count INT) |


# Schémas des bases de données SQL pour d'autres usages :

| Type de table  | Schéma |
| ------------- | ------------- |
| commandes  | CREATE TABLE commandes (MessageID BIGINT, AuthorID BIGINT, Commande TEXT, Option TEXT, Args1 TEXT, Args2 TEXT, Args3 TEXT, Args4 TEXT, Page INT, PageMax INT, Tri TEXT, Mobile BOOL) |
| graphiques  | CREATE TABLE graphs (MessageID BIGINT, Graph1 TEXT, Graph2 TEXT, Graph3 TEXT, Graph4 TEXT, Graph5 TEXT, Graph6 TEXT, Graph7 TEXT, Page INT, PageMax INT) |
| commandes custom | CREATE TABLE custom (Nom TEXT PRIMARY KEY, Description TEXT, Embed BOOL, Title TEXT, Author TEXT, Color TEXT, Footer TEXT, Image TEXT, Miniature TEXT) |
| giveaway | CREATE TABLE liste (Nombre INT PRIMARY KEY, IDMess BIGINT, IDChan INT) |



# Schémas des bases de données SQL pour les paramètres de chaque serveur :

| Type de table  | Schéma |
| ------------- | ------------- |
| commandes auto  | CREATE TABLE auto (Commande TEXT PRIMARY KEY, Salon BIGINT, Active BOOL) |
| salons H/B/M  | CREATE TABLE chans (ID BIGINT PRIMARY KEY, Hide BOOL, Blind BOOL, Mute BOOL) |
| modules | CREATE TABLE modulesCMD (Module TEXT, Statut BOOL) |
| savezvous | CREATE TABLE savezvous (Texte TEXT, ID BIGINT, Image TEXT, Count INT) |
| tableaux | CREATE TABLE sb (Nombre INT, Salon BIGINT, Emote TEXT, ID BIGINT, Count INT, PRIMARY KEY(Salon,Emote)) |
| membres H/B | CREATE TABLE users (ID BIGINT PRIMARY KEY, Hide BOOL, Blind BOOL, Leave BOOL) |
