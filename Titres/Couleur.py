from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Stats.SQL.ConnectSQL import connectSQL

from Titres.Outils import createAccount


@OTCommand
async def setColor(interaction,bot,couleur):
    try:
        r,g,b=tuple(int(couleur[i:i+2], 16) for i in (1, 3, 5))
    except:
        raise AssertionError("Pour définir votre couleur, vous devez fournir une valeur hexadécimale, commençant par #.")

    try:
        assert r>=0 and r<=255
        assert g>=0 and g<=255
        assert b>=0 and b<=255
    except:
        raise AssertionError("Le nombre hexadécimal donné ne correspond pas.")

    connexionUser,curseurUser=connectSQL("OT",interaction.user.id,"Titres",None,None)
    createAccount(connexionUser,curseurUser)
    coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
    assert coins>=50, "Vous n'avez pas assez d'OT Coins !"
    curseurUser.execute("UPDATE coins SET Coins=Coins-50")
    connexionUser.commit()

    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    assert curseur.execute("SELECT * FROM custombans WHERE ID={0}".format(interaction.user.id)).fetchone()==None, "Vous êtes banni des outils de personnalisation."
    if curseur.execute("SELECT * FROM couleurs WHERE ID={0}".format(interaction.user.id)).fetchone()==None:
        curseur.execute("INSERT INTO couleurs VALUES({0},{1},{2},{3})".format(interaction.user.id,r,g,b))
    else:
        curseur.execute("UPDATE couleurs SET R={0}, G={1}, B={2} WHERE ID={3}".format(r,g,b,interaction.user.id))
    connexion.commit()
    hexcolor='%02x%02x%02x' % (r, g, b)
    
    embed=createEmbed("Modification couleur personnelle","Votre nouvelle couleur est #{0} !\nR : {1}\nG : {2}\nB : {3}".format(hexcolor,r,g,b),int(hexcolor,base=16),interaction.command.qualified_name,interaction.user)
    await interaction.response.send_message(embed=embed)
