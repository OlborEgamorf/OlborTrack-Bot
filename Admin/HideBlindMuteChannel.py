import discord
from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Core.OT import OlborTrack
from Core.OTGuild import OTGuildCMD
from Stats.SQL.ConnectSQL import connectLocal, connectSQL


@OTCommand
async def exeHBM(interaction:discord.Interaction,salon:discord.TextChannel,bot:OlborTrack,option:str,guild:OTGuildCMD):
    """Fonction qui permet de rendre masqué, bloqué ou muet des salons textuels pour un serveur.
    
    En argument avec la commande est donné un ou plusieurs salons.
    
    Si aucun argument n'est donné, envoie un embed avec la liste des salons touchés par l'état voulu
    
    Connexion à la base de données et reset dans l'objet OTGuild
    
    Commande Admin."""
    connexion,curseur=connectSQL(interaction.guild_id)
    dictEmbed={"Hide":"masqués","Blind":"bloqués","Mute":"muets","Tab":"tableau-masqués"}
    dictBool={False:"",True:"dé"}

    if salon==None:
        etat=curseur.execute("SELECT * FROM chans WHERE ID={0}".format(salon.id)).fetchone()
        curseur.execute("UPDATE chans SET {0}={1} WHERE ID={2}".format(option,bool(int(etat[option])-1),salon.id))
        descip="<#{0}> ({1}{2})".format(salon.id,dictBool[etat[option]],dictEmbed[option][0:-1])
    else:
        descip=""
        for i in curseur.execute("SELECT * FROM chans").fetchall():
            if i[option]==True:
                descip+="<#"+str(i["ID"])+">, "

    connexion.commit()
    guild.getHBM()
    assert descip!="", "Aucun salon n'est {0}".format(dictEmbed[option][0:-1])
    await interaction.response.send_message(embed=createEmbed("Salons "+dictEmbed[option],descip[0:-2],0x220cc9,interaction.command.name,interaction.guild))
