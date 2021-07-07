from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Embeds import createEmbed, exeErrorExcept,embedAssert

async def exeHBM(ctx,bot,option,guild):
    """Fonction qui permet de rendre masqué, bloqué ou muet des salons textuels pour un serveur.
    
    En argument avec la commande est donné un ou plusieurs salons.
    
    Si aucun argument n'est donné, envoie un embed avec la liste des salons touchés par l'état voulu
    
    Connexion à la base de données et reset dans l'objet OTGuild
    
    Commande Admin."""
    try:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        dictEmbed={"Hide":"masqués","Blind":"bloqués","Mute":"muets"}
        dictBool={False:"",True:"dé"}
        descip=""
        if ctx.message.channel_mentions==[]:
            for i in curseur.execute("SELECT * FROM chans").fetchall():
                if i[option]==True:
                    descip+="<#"+str(i["ID"])+">, "
        else:
            for i in ctx.message.channel_mentions:
                etat=curseur.execute("SELECT * FROM chans WHERE ID={0}".format(i.id)).fetchone()
                curseur.execute("UPDATE chans SET {0}={1} WHERE ID={2}".format(option,bool(int(etat[option])-1),i.id))
                descip+="<#"+str(i.id)+"> ({0}{1}), ".format(dictBool[etat[option]],dictEmbed[option][0:-1])
            connexion.commit()
            guild.getHBM()
        assert descip!="", "Aucun salon n'est {0}".format(dictEmbed[option][0:-1])
        embedTable=createEmbed("Salons "+dictEmbed[option],descip[0:-2],0x220cc9,ctx.invoked_with.lower(),ctx.guild)
    except AssertionError as er:
        embedTable=embedAssert(str(er))
    except:
        embedTable=await exeErrorExcept(ctx,bot,"")
    await ctx.send(embed=embedTable)