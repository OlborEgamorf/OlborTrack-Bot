from Stats.SQL.NewSalons import addChan
from Stats.SQL.NewMembres import leaveUser
import os

dictOptions={"Messages":9,"Salons":0,"Freq":2,"Mots":6,"Emotes":8,"Reactions":3,"Voice":5,"Voicechan":5,"Mentions":4,"Mentionne":4,"Divers":10,"Moyennes":1,"Roles":7}

def verifExecSQL(guild,channel,author):
    if guild.gd or not guild.stats or os.path.exists("SQL/{0}/GETING".format(guild.id)):
        return False
    try:
        if guild.users[author.id]["Blind"]:
            return False
    except:
        if author.bot:
            return False
        leaveUser(guild,author,False)
    try:
        if guild.chan[channel.id]["Blind"]:
            return False
    except:
        addChan(guild,channel)
    return True

def verifExecGD(guild,channel,author):
    try:
        if guild.users[author.id]["Blind"]==True:
            return False
    except:
        if author.bot:
            return False
        leaveUser(guild,author,False)
    try:
        if guild.chan[channel.id]["Blind"]==True:
            return False
    except:
        addChan(guild,channel)
    return True

def verifCommands(guild,option):
    return guild.mstats[dictOptions[option]]["Statut"]