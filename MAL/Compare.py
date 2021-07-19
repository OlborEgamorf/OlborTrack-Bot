import discord
from Core.Fonctions.WebRequest import webRequest
from Core.Fonctions.Divers3 import lignesEmbed
from Core.Fonctions.AuteurIcon import auteur

async def embedMALcompare(user1,user2,genre,key,page):
    table,descip=[],""
    listeUsers=[user1,user2]
    for i in range(2):
        search=await webRequest("https://api.jikan.moe/v3/user/"+listeUsers[i].lower()+"/"+genre.lower()+"list/"+key.lower())
        assert search!=False, "Je ne trouve pas un des utilisateurs, ou alors la liste d'un des utilisateurs que vous cherchez est vide : "+listeUsers[i]+" !"
        table.append(search)
    i,longueur=0,len(table[0][genre.lower()])
    while i<longueur:
        add,h=False,0
        while add==False and h<len(table[1][genre.lower()]):
            if table[0][genre.lower()][i]["title"]==table[1][genre.lower()][h]["title"]:
                add=True
            h+=1
        if add==False:
            del table[0][genre.lower()][i]
            i,longueur=i-1,longueur-1
        i+=1
    assert table[0][genre.lower()]!=[],"Ces deux utilisateurs n'ont rien en commun dans cette liste..."
    generation=lignesEmbed(15,table[0][genre.lower()],page)
    debut,borne,pageT=generation[0],generation[1],generation[2]
    for i in range(debut,borne):
        descip+="["+table[0][genre.lower()][i]["title"]+"]("+table[0][genre.lower()][i]["url"]+") \n"
    embedMAL=discord.Embed(title="Comparaison entre {0} et {1}\n{2}, {3}".format(user1,user2,genre.lower(),key.lower()), description=descip, color=0x7c0cb0)
    embedMAL.set_footer(text="Page "+str(page+1)+"/"+str(pageT))
    embedMAL=auteur(0,0,0,embedMAL,"mal")
    return embedMAL,pageT