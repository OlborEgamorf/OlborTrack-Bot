from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.GetNom import getAuthor
from Core.Decorator import OTCommand
from Stats.SQL.ConnectSQL import connectSQL

@OTCommand
async def exeHBM(ctx,bot,option,guild):
    """Fonction qui permet de rendre masqué, bloqué ou muet des salons textuels pour un serveur.
    
    En argument avec la commande est donné un ou plusieurs salons.
    
    Si aucun argument n'est donné, envoie un embed avec la liste des salons touchés par l'état voulu
    
    Connexion à la base de données et reset dans l'objet OTGuild
    
    Commande Admin."""
    connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
    dictEmbed={"Hide":"masqués","Blind":"bloqués","Mute":"muets","Tab":"tableau-masqués"}
    dictBool={False:"",True:"dé"}
    descip=""

    if ctx.message.channel_mentions!=[]:
        for i in ctx.message.channel_mentions:
            etat=curseur.execute("SELECT * FROM chans WHERE ID={0}".format(i.id)).fetchone()
            curseur.execute("UPDATE chans SET {0}={1} WHERE ID={2}".format(option,bool(int(etat[option])-1),i.id))
            descip+="<#{0}> ({1}{2}), ".format(i.id,dictBool[etat[option]],dictEmbed[option][0:-1])
    elif len(ctx.args)>2:
        chan=getAuthor("Voicechan",ctx,2)
        etat=curseur.execute("SELECT * FROM chans WHERE ID={0}".format(chan)).fetchone()
        curseur.execute("UPDATE chans SET {0}={1} WHERE ID={2}".format(option,bool(int(etat[option])-1),chan))
        descip+="<#{0}> ({1}{2}), ".format(chan,dictBool[etat[option]],dictEmbed[option][0:-1])
    else:
        for i in curseur.execute("SELECT * FROM chans").fetchall():
            if i[option]==True:
                descip+="<#"+str(i["ID"])+">, "

    connexion.commit()
    guild.getHBM()
    assert descip!="", "Aucun salon n'est {0}".format(dictEmbed[option][0:-1])
    await ctx.reply(embed=createEmbed("Salons "+dictEmbed[option],descip[0:-2],0x220cc9,ctx.invoked_with.lower(),ctx.guild))
