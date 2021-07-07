from Stats.SQL.NewSalons import addChan
from Stats.SQL.NewMembres import leaveUser
import os

def verifExecSQL(guild,channel,author):
    if os.path.exists("SQL/"+str(guild.id)+"/GETING")==True:
        return False
    try:
        if guild.users[author.id]["Blind"]==True:
            return False
    except:
        leaveUser(guild,author,False)
    try:
        if guild.chan[channel.id]["Blind"]==True:
            return False
    except:
        addChan(guild,channel)
    return True

def verifExecGD(guild,channel,author):
    try:
        if guild.users[author.id]["Blind"]==True:
            return False
    except:
        leaveUser(guild,author,False)
    try:
        if guild.chan[channel.id]["Blind"]==True:
            return False
    except:
        addChan(guild,channel)
    return True