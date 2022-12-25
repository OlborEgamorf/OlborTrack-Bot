from time import strftime
from Titres.Outils import getColorJeux
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Embeds import createEmbed, defEvol
from Core.Fonctions.TempsVoice import tempsVoice
from Titres.Badges import getBadges
from Core.Fonctions.GetNom import getTitre

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def commandeCount(interaction):
    embed=createEmbed("Compteurs","",interaction.user.color.value,"count",interaction.user)
    connexion,curseur=connectSQL(interaction.guild_id)
    for i in ("Messages","Mots","Voice"):
        descip=""
        try:
            glob=curseur.execute("SELECT * FROM glob WHERE ID={0}".format(interaction.user.id)).fetchone()
            if glob!=None:
                count=tempsVoice(glob["Count"]) if i=="Voice" else glob["Count"]
                descip+="**Global** : {0} - {1}e {2}\n".format(count,glob["Rank"],defEvol(glob,True))
        except:
            pass

        try:
            annee=curseur.execute("SELECT * FROM to{0} WHERE ID={1}".format(strftime("%y"),interaction.user.id)).fetchone()
            if annee!=None:
                count=tempsVoice(annee["Count"]) if i=="Voice" else annee["Count"]
                descip+="**20{0}** : {1} - {2}e {3}\n".format(strftime("%y"),count,annee["Rank"],defEvol(annee,True))
        except:
            pass

        try:
            mois=curseur.execute("SELECT * FROM {0}{1} WHERE ID={2}".format(tableauMois[strftime("%m")].lower(),strftime("%y"),interaction.user.id)).fetchone()
            if mois!=None:
                count=tempsVoice(mois["Count"]) if i=="Voice" else mois["Count"]
                descip+="**{0} 20{1}** : {2} - {3}e {4}\n".format(tableauMois[strftime("%m")],strftime("%y"),count,mois["Rank"],defEvol(mois,True))
        except:
            pass
        
        if descip!="":
            embed.add_field(name=i,value=descip,inline=True)
    await interaction.response.send_message(embed=embed)


async def jeuxPerso(interaction):
    connexion,curseur=connectSQL("OT")
    embed=createEmbed("Tableau jeux - perso","",getColorJeux(interaction.user.id,curseur),interaction.command.name,interaction.user)
    
    for i in ["P4","BatailleNavale","Tortues","TortuesDuo","TrivialVersus","TrivialParty","TrivialBR","Matrice"]:
        descip=""
        try:
            glob=curseur.execute("SELECT * FROM glob WHERE ID={0}".format(interaction.user.id)).fetchone()
            if glob!=None:
                descip+="**Global** : {0} - {1}e {2}\n".format(glob["Count"],glob["Rank"],defEvol(glob,True))
        except:
            pass

        try:
            annee=curseur.execute("SELECT * FROM to{0} WHERE ID={1}".format(strftime("%y"),interaction.user.id)).fetchone()
            if annee!=None:
                descip+="**20{0}** : {1} - {2}e {3}\n".format(strftime("%y"),annee["Count"],annee["Rank"],defEvol(annee,True))
        except:
            pass

        try:
            mois=curseur.execute("SELECT * FROM {0}{1} WHERE ID={2}".format(tableauMois[strftime("%m")].lower(),strftime("%y"),interaction.user.id)).fetchone()
            if mois!=None:
                descip+="**{0} 20{1}** : {2} - {3}e {4}\n".format(tableauMois[strftime("%m")],strftime("%y"),mois["Count"],mois["Rank"],defEvol(mois,True))
        except:
            pass
        
        if descip!="":
            embed.add_field(name=i,value=descip,inline=True)
    await interaction.response.send_message(embed=embed)


async def jeuxBoard(interaction,bot):
    embed=createEmbed("Tableau jeux - premiers","",0x3498db,interaction.command.name,bot.user)
    connexion,curseur=connectSQL("OT")
    for i in ["P4","Tortues","TortuesDuo","TrivialVersus","TrivialParty","TrivialBR","Matrice","Morpion","CodeNames"]:
        descip=""
        try:
            glob=curseur.execute("SELECT * FROM glob WHERE Rank=1").fetchone()
            if glob!=None:
                descip+="**Global** : {0} {1} - {2} points\n".format(getBadges(glob["ID"],i),getTitre(curseur,glob["ID"]),glob["Count"])
        except:
            pass

        try:
            annee=curseur.execute("SELECT * FROM to{0} WHERE Rank=1".format(strftime("%y"))).fetchone()
            if annee!=None:
                descip+="**20{0}** : {1} {2} - {3} points\n".format(strftime("%y"),getBadges(annee["ID"],i),getTitre(curseur,annee["ID"]),annee["Count"])
        except:
            pass

        try:
            mois=curseur.execute("SELECT * FROM {0}{1} WHERE Rank=1".format(tableauMois[strftime("%m")].lower(),strftime("%y"))).fetchone()
            if mois!=None:
                descip+="**{0} 20{1}** : {2} {3} - {4} points\n".format(tableauMois[strftime("%m")],strftime("%y"),getBadges(mois["ID"],i),getTitre(curseur,mois["ID"]),mois["Count"])
        except:
            pass
        
        if descip!="":
            embed.add_field(name=i,value=descip,inline=True)
    await interaction.response.send_message(embed=embed)