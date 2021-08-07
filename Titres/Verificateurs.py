from Stats.SQL.ConnectSQL import connectSQL
from Titres.Outils import createAccount

dictValue={1:300,2:800,3:5000}
dictSell={1:150,2:400,3:2500}

def verifAchat(ctx,idtitre,gift):
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    titre=curseur.execute("SELECT marketplace.ID,marketplace.Stock,titres.Rareté,titres.Nom FROM marketplace JOIN titres ON marketplace.ID=titres.ID WHERE marketplace.ID={0}".format(idtitre)).fetchone()
    assert titre!=None, "Ce titre n'est actuellement pas en vente !"
    assert titre["Stock"]!=0, "Ce titre n'est plus en stock sur le MarketPlace !"

    connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
    createAccount(connexionUser,curseurUser)
    coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
    assert coins>=dictValue[titre["Rareté"]], "Vous n'avez pas assez d'OT Coins pour acheter ce titre !"

    if gift:
        connexionGift,curseurGift=connectSQL("OT",ctx.message.mentions[0].id,"Titres",None,None)
        createAccount(connexionGift,curseurGift)
        assert curseurGift.execute("SELECT * FROM titresUser WHERE ID={0}".format(idtitre)).fetchone()==None, "La personne à qui vous voulez offrir ce titre le possède déjà !"
        if titre["Rareté"]==3:
            assert curseurGift.execute("SELECT COUNT() FROM titresUser WHERE Rareté=3").fetchone()==0, "La personne à qui vous voulez offrir ce titre a déjà un titre de type Unique."
        connexionGift.close()
    else:
        assert curseurUser.execute("SELECT * FROM titresUser WHERE ID={0}".format(idtitre)).fetchone()==None, "Vous possèdez déjà ce titre !"
        if titre["Rareté"]==3:
            assert curseurUser.execute("SELECT COUNT() FROM titresUser WHERE Rareté=3").fetchone()==0, "Vous ne pouvez pas avoir plus d'un titre unique dans votre inventaire."

    connexionUser.close()
    connexion.close()
    return titre["Nom"], dictValue[titre["Rareté"]], coins

def verifVente(ctx,idtitre):
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
    createAccount(connexionUser,curseurUser)

    titre=curseurUser.execute("SELECT * FROM titresUser WHERE ID={0}".format(idtitre)).fetchone()
    assert titre!=None, "Vous ne possèdez pas ce titre."
    assert curseur.execute("SELECT * FROM active WHERE MembreID={0}".format(ctx.author.id)).fetchone()["TitreID"]!=int(idtitre), "Le titre que vous voulez vendre est celui qui est actuellement équipé pour vous."

    coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]

    connexionUser.close()
    connexion.close()
    return titre["Nom"], dictSell[titre["Rareté"]], coins