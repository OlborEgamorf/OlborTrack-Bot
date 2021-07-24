from Stats.SQL.ConnectSQL import connectSQL
from Core.Reactions.ChangePage import reactStats
import discord
from discord.ext import commands
from Core.OTGuild import OTGuild

async def changeTri(message:discord.Message,reaction:discord.Reaction,user:discord.Member,bot:commands.Bot,guildOT:OTGuild):
    """Modifie le tri d'une commande en fonction de son type, et de la boucle d'où elle se trouve.
    
    Vérifie d'abord si le message est enregistré dans la base de données des commandes du serveur, puis fait les modifications nécessaires et renvoie la commande avec le nouveau tri."""
    connexionCMD,curseurCMD=connectSQL(message.guild.id,"Commandes","Guild",None,None)
    ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(message.id)).fetchone()
    if ligne!=None:
        if ligne["Commande"] in ("rank","roles"):
            dictNext={"countDesc":"countAsc","countAsc":"countDesc"}
        elif ligne["Commande"] in ("periods","periodsInter"):
            dictNext={"countDesc":"periodAsc","periodAsc":"periodDesc","periodDesc":"rankAsc","rankAsc":"countDesc"}
        elif ligne["Commande"]=="perso":
            dictNext={"countDesc":"rankAsc","rankAsc":"countAsc","countAsc":"rankDesc","rankDesc":"countDesc"}
        elif ligne["Commande"]=="evol":
            dictNext={"dateAsc":"dateDesc","dateDesc":"rankAsc","rankAsc":"dateAsc"}
        elif ligne["Commande"]=="day":
            dictNext={"dateAsc":"dateDesc","dateDesc":"countDesc","countDesc":"countAsc","countAsc":"dateAsc"}
        elif ligne["Commande"]=="moy":
            dictNext={"moyDesc":"periodDesc","periodDesc":"periodAsc","periodAsc":"countDesc","countDesc":"nombreDesc","nombreDesc":"moyDesc"}
        elif ligne["Commande"]=="jeux":
            dictNext={"countDesc":"winDesc","winDesc":"loseDesc","loseDesc":"countAsc","countAsc":"winAsc","winAsc":"loseAsc","loseAsc":"countDesc"}
        elif ligne["Commande"]=="trivial" and ligne["Option"]=="trivial":
            dictNext={"countDesc":"countAsc","countAsc":"countDesc"}
        elif ligne["Commande"]=="trivial" and ligne["Option"]=="trivialperso":
            dictNext={"expDesc":"expAsc","expAsc":"expDesc"}
        elif ligne["Commande"]=="compareUser" and ligne["Args1"] in ("user","userObj"):
            dictNext={"countDesc":"periodAsc","periodAsc":"periodDesc","periodDesc":"rankAsc","rankAsc":"countDesc"}
        elif ligne["Commande"] in ("compareUser","comparePerso","compareRank","compareServ"):
            dictNext={"countDesc":"countAsc","countAsc":"countDesc"}
        
        curseurCMD.execute("UPDATE commandes SET Tri='{0}' WHERE MessageID={1}".format(dictNext[ligne["Tri"]],message.id))
        connexionCMD.commit()
        await reactStats(message,reaction,user,bot,guildOT)