from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.EmoteDetector import emoteDetector

from Titres.Outils import createAccount


@OTCommand
async def setEmote(interaction,bot,emote):
    emote=emoteDetector(emote)
    assert len(emote)!=0, "Vous devez me donner l'emote que vous voulez équiper !"
    emoteBot=bot.get_emoji(int(emote[0]))
    assert emoteBot!=None, "Vous devez me donner une emote que je connais et qui est visible à mes yeux !\nAttention : si vous venez de la créer, il est possible qu'il y est des soucis de synchronisation."

    connexionUser,curseurUser=connectSQL("OT",interaction.user.id,"Titres",None,None)
    createAccount(connexionUser,curseurUser)
    coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
    assert coins>=50, "Vous n'avez pas assez d'OT Coins !"
    curseurUser.execute("UPDATE coins SET Coins=Coins-50")
    connexionUser.commit()
    
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    assert curseur.execute("SELECT * FROM custombans WHERE ID={0}".format(interaction.user.id)).fetchone()==None, "Vous êtes banni des outils de personnalisation."
    if curseur.execute("SELECT * FROM emotes WHERE ID={0}".format(interaction.user.id)).fetchone()==None:
        curseur.execute("INSERT INTO emotes VALUES({0},'{1}',{2})".format(interaction.user.id,str(emoteBot),emoteBot.id))
    else:
        curseur.execute("UPDATE emotes SET Nom='{0}', IDEmote={1} WHERE ID={2}".format(str(emoteBot),emoteBot.id,interaction.user.id))
    connexion.commit()

    embed=createEmbed("Modification emote personnelle","Votre nouvelle emote est {0} !".format(str(emoteBot)),0xf58d1d,interaction.command.qualified_name,interaction.user)
    await interaction.response.send_message(embed=embed)
    #await bot.get_channel(750803643820802100).send("Emote : {0} - {1}".format(interaction.user.id,str(emoteBot)))
