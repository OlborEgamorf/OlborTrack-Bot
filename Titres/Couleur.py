import discord
from Core.Fonctions.Embeds import createEmbed, embedAssert
from Stats.SQL.ConnectSQL import connectSQL


async def setColor(ctx,bot,args):
    try:
        if len(args)==1:
            r,g,b=tuple(int(args[0][i:i+2], 16) for i in (1, 3, 5))
        elif len(args)>=3:
            r=int(args[0])
            g=int(args[1])
            b=int(args[2])
        else:
            raise AssertionError("Pour définir votre couleur, vous devez fournir une valeur hexadécimale, commençant par # ou alors les valeurs Rouge, Verte et Bleu qui la compose. Les valeurs doivent être comprises entre 0 et 255.")
        try:
            assert r>=0 and r<=255
            assert g>=0 and g<=255
            assert b>=0 and b<=255
        except:
            raise AssertionError("Les valeurs données doivent être des nombres, compris entre 0 et 255.")

        connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
        if curseur.execute("SELECT * FROM couleurs WHERE ID={0}".format(ctx.author.id)).fetchone()==None:
            curseur.execute("INSERT INTO couleurs VALUES({0},{1},{2},{3})".format(ctx.author.id,r,g,b))
        else:
            curseur.execute("UPDATE couleurs SET R={0}, G={1}, B={2} WHERE ID={3}".format(r,g,b,ctx.author.id))
        connexion.commit()
        hexcolor='%02x%02x%02x' % (r, g, b)
        embed=createEmbed("Modification couleur personnelle","Votre nouvelle couleur est #{0} !\nR : {1}\nG : {2}\nB : {3}".format(hexcolor,r,g,b),int(hexcolor,base=16),"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
        await ctx.send(embed=embed)
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))


def getColorJeux(user):
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    couleur=curseur.execute("SELECT * FROM couleurs WHERE ID={0}".format(user)).fetchone()
    if couleur==None:
        return None
    return int('%02x%02x%02x' % (couleur["R"], couleur["G"], couleur["B"]),base=16)
