from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.EmoteDetector import emoteDetector

from Titres.Outils import createAccount


@OTCommand
async def setEmote(ctx,bot,args):
    assert len(args)!=0, "Vous devez me donner l'emote que vous voulez équiper !"
    emote=emoteDetector(args[0])
    assert len(emote)!=0, "Vous devez me donner l'emote que vous voulez équiper !"
    emoteBot=bot.get_emoji(int(emote[0]))
    assert emoteBot!=None, "Vous devez me donner une emote que je connais et qui est visible à mes yeux !\nAttention : si vous venez de la créer, il est possible qu'il y est des soucis de synchronisation."

    connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
    createAccount(connexionUser,curseurUser)
    coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
    assert coins>=50, "Vous n'avez pas assez d'OT Coins !"
    curseurUser.execute("UPDATE coins SET Coins=Coins-50")
    connexionUser.commit()
    
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    assert curseur.execute("SELECT * FROM custombans WHERE ID={0}".format(ctx.author.id)).fetchone()==None, "Vous êtes banni des outils de personnalisation."
    if curseur.execute("SELECT * FROM emotes WHERE ID={0}".format(ctx.author.id)).fetchone()==None:
        curseur.execute("INSERT INTO emotes VALUES({0},'{1}',{2})".format(ctx.author.id,str(emoteBot),emoteBot.id))
    else:
        curseur.execute("UPDATE emotes SET Nom='{0}', IDEmote={1} WHERE ID={2}".format(str(emoteBot),emoteBot.id,ctx.author.id))
    connexion.commit()
    embed=createEmbed("Modification emote personnelle","Votre nouvelle emote est {0} !".format(str(emoteBot)),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
    await ctx.send(embed=embed)
    await bot.get_channel(750803643820802100).send("Emote : {0} - {1}".format(ctx.author.id,str(emoteBot)))

def getEmoteJeux(user):
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    emote=curseur.execute("SELECT * FROM emotes WHERE ID={0}".format(user)).fetchone()
    if emote==None:
        return None
    return emote["Nom"]
