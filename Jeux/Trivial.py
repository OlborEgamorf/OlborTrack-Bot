############################################################################

 #######  #########     #########       #######
#       #     #                 #            #     Olbor Track Bot    
#       #     #                 #           #      Créé par OlborEgamorf  
#       #     #         #########          #       Fonctions Trivial
#       #     #         #                 #                  
 #######      #         ############# #  #                         

############################################################################

import asyncio
import html
import sqlite3
import sys
from random import choice, randint
from time import strftime

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.DichoTri import triID
from Core.Fonctions.Embeds import embedAssert, exeErrorExcept, createEmbed
from Stats.SQL.Compteur import compteurSQL, compteurTrivialS
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeJeuxSQL
from Titres.Outils import gainCoins, titresTrivial

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>"]
emotesTrue=["<:ot1VRAI:773993429130149909>", "<:ot2VRAI:773993429050195979>", "<:ot3VRAI:773993429331738624>", "<:ot4VRAI:773993429423095859>"]
emotesFalse=["<:ot1FAUX:773993429315092490>", "<:ot2FAUX:773993429172486145>", "<:ot3FAUX:773993429402779698>", "<:ot4FAUX:773993429373026354>"]
listeNoms=["Culture","Divertissement","Sciences","Mythologie","Sport","Géographie","Histoire","Politique","Art","Célébrités","Animaux","Véhicules","Global"]
dictCateg={9:0,10:1,11:1,12:1,13:1,14:1,15:1,16:1,17:2,18:2,19:2,20:3,21:4,22:5,23:6,24:7,25:8,26:9,27:10,28:11,29:1,30:2,31:1,32:1}
dictDiff={"easy":"Facile (+10)","medium":"Moyenne (+15)","hard":"Difficile (+25)"}





