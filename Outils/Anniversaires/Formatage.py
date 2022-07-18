from time import strftime
import discord

def formatageAnniv(alerte:str,user:discord.Member):

    alerte=alerte.replace("{user}","<@{0}>".format(user.id))
    alerte=alerte.replace("{name}",user.name)
    alerte=alerte.replace("{date}",strftime("%d/%m/20%y"))
    
    return alerte