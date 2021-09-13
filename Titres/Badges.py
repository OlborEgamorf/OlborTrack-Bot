from Core.Fonctions.Embeds import createEmbed, embedAssert
from Stats.SQL.ConnectSQL import connectSQL

dictValues={1:"<:BronzeMois:886707210749632542>",2:"<:ArgentMois:886707209797521448>",3:"<:OrMois:886707210472800276>",11:"<:BronzeAnnee:886707210560884776>",12:"<:ArgentAnnee:886707209965277225>",13:"<:OrAnnee:886707210430840862>",101:"<:SaphirGlobal:886707210409893958>",102:"<:RubisGlobal:886707210225332255>",103:"<:DiamantGlobal:886707210560884778>"}

async def showBadges(ctx,bot):
    try:
        connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
        liste=["P4","BatailleNavale","Tortues","TortuesDuo","TrivialVersus","TrivialParty","TrivialBR","Matrice"]
        liste.sort()
        listeValues=[1,2,3,11,12,13]
        descip=""
        for i in liste:
            descip+="**{0}** : ".format(i)
            for j in listeValues:
                if curseurUser.execute("SELECT * FROM badges WHERE Type='{0}' AND Valeur={1}".format(i,j)).fetchone()==None:
                    descip+="<:BadgeVide:886707210003025982> "
                else:
                    descip+="{0} ".format(dictValues[j])
            if curseurUser.execute("SELECT * FROM badges WHERE Type='{0}' AND (Valeur=101 OR Valeur=102 OR Valeur=103)".format(i,j)).fetchone()!=None:
                descip+="{0} ".format(dictValues[curseurUser.execute("SELECT * FROM badges WHERE Type='{0}' AND (Valeur=101 OR Valeur=102 OR Valeur=103)".format(i,j)).fetchone()["Valeur"]])
            descip+="\n"
            
        if curseurUser.execute("SELECT * FROM badges WHERE Période='VIP'").fetchone()==None:
            descip+="\n***VIP*** : <:VIPVide:886707613260193853>\n"
        else:
            descip+="\n***VIP*** : <:VIP:886707613667049533>\n"
        
        if curseurUser.execute("SELECT * FROM badges WHERE Période='Testeur'").fetchone()==None:
            descip+="***Testeur*** : <:TesteurVide:886707613260218398>\n"
        else:
            descip+="***Testeur*** : <:Testeur:886707613792862250>\n"

        await ctx.reply(embed=createEmbed("Vos badges",descip,ctx.author.color.value,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author))
    except:
        await ctx.reply(embed=embedAssert("Vous n'avez aucun badge visiblement..."))


def getBadges(user,jeu):
    try:
        connexionUser,curseurUser=connectSQL("OT",user,"Titres",None,None)
        descip=""
        main=curseurUser.execute("SELECT * FROM badges WHERE Type='{0}' ORDER BY Valeur DESC".format(jeu)).fetchone()
        if main!=None:
            descip+=dictValues[main["Valeur"]]
        if curseurUser.execute("SELECT * FROM badges WHERE Période='VIP'").fetchone()!=None:
            descip+="<:VIP:886707613667049533>"
        if curseurUser.execute("SELECT * FROM badges WHERE Période='Testeur'").fetchone()!=None:
            descip+="<:Testeur:886707613792862250>"
        return descip
    except:
        return ""